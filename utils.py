import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tavily import TavilyClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import List
from schemas import DomainInfo, Competitor, CompetitorList  # Ensure this import is at the top to avoid circular dependencies

# Updated imports to address deprecation warnings
from langchain_community.document_loaders import UnstructuredURLLoader, UnstructuredPDFLoader
from langchain_community.embeddings import FastEmbedEmbeddings

# Initialize in the global scope to avoid re-initializing in multiple functions
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not tavily_api_key or not groq_api_key:
    raise ValueError("TAVILY_API_KEY and GROQ_API_KEY must be set in the .env file")

# Initialize Tavily and Groq
tavily = TavilyClient(api_key=tavily_api_key)
llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")  # Or any other supported Groq model

# Constants
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def tavily_search(query: str, search_depth="advanced"):
    """Searches Tavily for the given query."""
    try:
        results = tavily.search(query=query, search_depth=search_depth)
        # Adjust based on actual API response structure
        return results.get('results', []) if isinstance(results, dict) else []
    except Exception as e:
        print(f"Tavily Search Error: {e}")
        return []


def load_and_chunk_data(url: str, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Loads data from a URL and chunks it for LLM processing."""
    try:
        if url.endswith('.pdf'):
            loader = UnstructuredPDFLoader(url)
        else:
            loader = UnstructuredURLLoader(urls=[url])
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        all_splits = text_splitter.split_documents(data)
        return all_splits
    except Exception as e:
        print(f"Error loading and chunking data from {url}: {e}")
        return []


def create_vectorstore(chunks: List[str], embeddings: FastEmbedEmbeddings):
    """Creates a vectorstore from the given chunks."""
    try:
        if not chunks:
            print("No chunks to create vectorstore.")
            return None
        
        # Import here to ensure it's loaded after installation
        from langchain_community.vectorstores import Chroma
        db = Chroma.from_documents(chunks, embeddings)
        return db
    except ImportError:
        print("Error: Please ensure chromadb is installed correctly")
        return None
    except Exception as e:
        print(f"Error creating vectorstore: {e}")
        return None


def retrieve_context(db, query, k=3):
    """Retrieves context from the vectorstore based on the query."""
    try:
        if not db:
            print("Vectorstore is None. Cannot retrieve context.")
            return ""
        docs = db.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return ""


def create_domain_summary(company_name: str, domain: str, context: str):
    """Creates a domain summary using the LLM."""
    prompt = f"""You are a research assistant tasked with creating a summary of the following domain for {company_name}: {domain}.
Your summary should cover the key aspects of the domain, including relevant metrics, trends, and competitors.
Use the following context to create the summary:

{context}
Include news_links in your summary if available.
Return your answer in markdown format:"""

    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error creating domain summary for {domain}: {e}")
        return ""


def extract_domain_info(company_name: str, domain: str, context: str):
    """Extracts structured information for a specific domain using the LLM."""
    parser = PydanticOutputParser(pydantic_object=DomainInfo)

    prompt = PromptTemplate(
        template="""You are a research assistant tasked with extracting information about {company_name} in the {domain} domain.
You should use the following context to extract the information. If the information isn't available respond with 'NA'. 

{context}

You must respond in a JSON format that adheres to the following schema:
{format_instructions}
""",
        input_variables=["company_name", "domain", "context"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    try:
        chain = prompt | llm | parser
        raw_output = chain.invoke({"company_name": company_name, "domain": domain, "context": context})
        output = raw_output.dict(exclude_none=True)

        # Sanitize the output to handle "NA" values for lists
        for key, value in output.get("key_metrics", {}).items():
            if value == "NA":
                output["key_metrics"][key] = None

        list_fields = ["market_trends", "competitors", "legal_issues", "news_links"]
        for field in list_fields:
            if field in output and output[field] == "NA":
                output[field] = []

        return output
    except Exception as e:
        print(f"Error extracting {domain} information: {e}")
        return {}


def extract_competitor_info(company_name: str, context: str):
    """Extracts structured information for competitors using the LLM."""
    parser = PydanticOutputParser(pydantic_object=CompetitorList)

    prompt = PromptTemplate(
        template="""You are a research assistant tasked with extracting information about competitors of {company_name}.
You should use the following context to extract the information. If a competitor isn't mentioned or information isn't available, respond with 'NA'.

{context}

You must respond in a JSON format that adheres to the following schema:
{format_instructions}
""",
        input_variables=["company_name", "context"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    try:
        chain = prompt | llm | parser
        raw_output = chain.invoke({"company_name": company_name, "context": context})
        output = raw_output.dict(exclude_none=True)

        # Sanitize the output
        for competitor in output.get("competitors", []):
            for key, value in competitor.get("key_metrics", {}).items():
                if value == "NA":
                    competitor["key_metrics"][key] = None

        return output.get("competitors", [])

    except Exception as e:
        print(f"Error extracting competitor information: {e}")
        return []