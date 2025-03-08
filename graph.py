from langchain_core.runnables import chain
from langgraph.graph import StateGraph, END
from utils import (
    tavily_search,
    load_and_chunk_data,
    create_vectorstore,
    retrieve_context,
    extract_domain_info,
    extract_competitor_info,
    FastEmbedEmbeddings,
)
from dataclasses import dataclass, field
import yaml

# Define the state of the graph using dataclasses for type safety
@dataclass
class AgentState:
    company_name: str
    results: dict = field(default_factory=dict)

    def __repr__(self):
        return f"AgentState(company_name={self.company_name}, results={self.results.keys() if self.results else None})"


# Define nodes (functions) in the graph
def check_company_exists(state: AgentState):
    company_name = state.company_name
    search_results = tavily_search(f"Is {company_name} a real company?")
    exists = bool(search_results)
    state.results["exists"] = exists
    return {"exists": exists}


def research_finance(state: AgentState):
    company_name = state.company_name
    domain = "finance"
    search_query = f"{company_name} {domain} analysis"
    search_results = tavily_search(search_query)

    if not search_results:
        print(f"No search results found for domain: {domain}")
        return {"finance": {}}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, search_query)
    if not context:
        return {"finance": {}}

    domain_info = extract_domain_info(company_name, domain, context)
    state.results["finance"] = domain_info
    return {"finance": domain_info}


def research_markets(state: AgentState):
    company_name = state.company_name
    domain = "markets"
    search_query = f"{company_name} {domain} analysis"
    search_results = tavily_search(search_query)

    if not search_results:
        print(f"No search results found for domain: {domain}")
        return {"markets": {}}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, search_query)
    if not context:
        return {"markets": {}}

    domain_info = extract_domain_info(company_name, domain, context)
    state.results["markets"] = domain_info
    return {"markets": domain_info}


def research_audience(state: AgentState):
    company_name = state.company_name
    domain = "audience"
    search_query = f"{company_name} {domain} analysis"
    search_results = tavily_search(search_query)

    if not search_results:
        print(f"No search results found for domain: {domain}")
        return {"audience": {}}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, search_query)
    if not context:
        return {"audience": {}}

    domain_info = extract_domain_info(company_name, domain, context)
    state.results["audience"] = domain_info
    return {"audience": domain_info}


def research_paralegal(state: AgentState):
    company_name = state.company_name
    domain = "paralegal"
    search_query = f"{company_name} {domain} analysis"
    search_results = tavily_search(search_query)

    if not search_results:
        print(f"No search results found for domain: {domain}")
        return {"paralegal": {}}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, search_query)
    if not context:
        return {"paralegal": {}}

    domain_info = extract_domain_info(company_name, domain, context)
    state.results["paralegal"] = domain_info
    return {"paralegal": domain_info}


def research_political(state: AgentState):
    company_name = state.company_name
    domain = "political"
    search_query = f"{company_name} {domain} analysis"
    search_results = tavily_search(search_query)

    if not search_results:
        print(f"No search results found for domain: {domain}")
        return {"political": {}}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, search_query)
    if not context:
        return {"political": {}}

    domain_info = extract_domain_info(company_name, domain, context)
    state.results["political"] = domain_info
    return {"political": domain_info}


def research_general(state: AgentState):
    company_name = state.company_name
    domain = "general"
    search_query = f"{company_name} {domain} analysis"
    search_results = tavily_search(search_query)

    if not search_results:
        print(f"No search results found for domain: {domain}")
        return {"general": {}}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, search_query)
    if not context:
        return {"general": {}}

    domain_info = extract_domain_info(company_name, domain, context)
    state.results["general"] = domain_info
    return {"general": domain_info}


def research_competitors(state: AgentState):
    company_name = state.company_name
    search_results = tavily_search(f"{company_name} competitors")

    if not search_results:
        print("No search results found for competitors.")
        return {"competitors": []}

    embeddings = FastEmbedEmbeddings()
    all_chunks = []
    for result in search_results:
        url = result.get('url')
        if url:
            chunks = load_and_chunk_data(url)
            all_chunks.extend(chunks)

    db = create_vectorstore(all_chunks, embeddings)
    context = retrieve_context(db, f"{company_name} competitors")
    if not context:
        return {"competitors": []}

    competitor_info = extract_competitor_info(company_name, context)
    state.results["competitors"] = competitor_info
    return {"competitors": competitor_info}


def format_results(state: AgentState):
    """Formats the collected information into a structured dictionary."""
    formatted_results = {
        "company_name": state.company_name,
        "exists": state.results.get("exists", False),
        "domains": {
            "finance": state.results.get("finance", {}),
            "markets": state.results.get("markets", {}),
            "audience": state.results.get("audience", {}),
            "paralegal": state.results.get("paralegal", {}),
            "political": state.results.get("political", {}),
            "general": state.results.get("general", {}),
        },
        "competitors": state.results.get("competitors", []),
    }
    return formatted_results


# Define the graph
builder = StateGraph(AgentState)
builder.add_node("check_exists", check_company_exists)
builder.add_node("research_finance", research_finance)
builder.add_node("research_markets", research_markets)
builder.add_node("research_audience", research_audience)
builder.add_node("research_paralegal", research_paralegal)
builder.add_node("research_political", research_political)
builder.add_node("research_general", research_general)
builder.add_node("research_competitors", research_competitors)
builder.add_node("format_results", format_results)

# Define edges
builder.add_edge("check_exists", "research_finance")  # If company exists, start finance research
builder.add_edge("research_finance", "research_markets")
builder.add_edge("research_markets", "research_audience")
builder.add_edge("research_audience", "research_paralegal")
builder.add_edge("research_paralegal", "research_political")
builder.add_edge("research_political", "research_general")
builder.add_edge("research_general", "research_competitors")
builder.add_edge("research_competitors", "format_results")  # Always format results.
builder.add_edge("format_results", END)

builder.set_entry_point("check_exists")

# Compile the graph
graph = builder.compile()


# Example usage
if __name__ == "__main__":
    company_name = "OpenAI"
    initial_state = AgentState(company_name=company_name)
    results = graph.invoke(initial_state)
    print(yaml.dump(results["formatted_results"], indent=2))