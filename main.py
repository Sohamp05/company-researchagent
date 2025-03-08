import os
import yaml
import logging
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from dataclasses import dataclass
from utils import tavily_search, load_and_chunk_data, create_vectorstore, retrieve_context, extract_domain_info, extract_competitor_info
from utils import FastEmbedEmbeddings
from graph import graph, AgentState  # Import what we need from graph.py

# Load environment variables
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not tavily_api_key or not groq_api_key:
    raise ValueError("TAVILY_API_KEY and GROQ_API_KEY must be set in the .env file")

# Function to run the agent with a given company name
def run_agent(company_name: str):
    # Initialize the agent state
    initial_state = AgentState(company_name=company_name)
    
    try:
        # Invoke the agent with the state and get the results
        results = graph.invoke(initial_state)
        research_results = results
        
        # Optionally, save the results to a YAML file (for debugging or further use)
        with open("research_results.yaml", "w") as outfile:
            yaml.dump(research_results, outfile, default_flow_style=False, indent=2)
        
        logging.info("Research complete. Results saved to research_results.yaml")
        
        return research_results  # Return the results as a Python dictionary (can be converted to JSON)
    except Exception as e:
        logging.error(f"Error during research: {e}")
        return {"error": str(e)}  # Return an error message if the research fails
