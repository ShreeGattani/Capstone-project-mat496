import os
from tavily import TavilyClient
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Annotated
from graph_state import GraphState  # Assuming you put the GraphState definition in graph_state.py

# --- Ingestor Node Function ---
def ingest_problem_context(state: GraphState) -> GraphState:
    """
    Ingests the problem statement from the URL and populates the problem_context field.
    This acts as the RAG step to give the LLM external knowledge.
    
    Args:
        state (GraphState): The current state of the graph.
    
    Returns:
        GraphState: The updated state with the problem_context.
    """
    print("---INGESTOR NODE: Retrieving Problem Context---")
    
    problem_url = state.get("problem_url")
    if not problem_url:
        raise ValueError("Problem URL is missing from the state.")

    try:
        # Use Tavily to retrieve processed content for the problem URL.
        tavily_api_key = os.getenv("TAVILY_API_KEY")
        if not tavily_api_key:
            raise ValueError("TAVILY_API_KEY is not set in the environment/.env file.")

        client = TavilyClient(api_key=tavily_api_key)

        # We query Tavily with the URL as the search query and request raw content.
        tavily_results = client.search(
            query=problem_url,
            include_raw_content=True,
            max_results=3,
            search_depth="advanced"
        )

        if not tavily_results or "results" not in tavily_results or len(tavily_results["results"]) == 0:
            raise ValueError("Tavily returned no results for the given problem URL.")

        # Concatenate the raw content from the top results.
        raw_texts = [r.get("raw_content") or r.get("content", "") for r in tavily_results["results"]]
        full_text = "\n".join([t for t in raw_texts if t])

        # Use a text splitter to keep context size manageable for the LLM.
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50
        )
        chunks = text_splitter.split_text(full_text)

        # Combine chunks into a single string for the LLM context.
        context = "\n".join(chunks)

        print(f"Successfully scraped {len(context)} characters of problem context.")
        
        return {
            "problem_context": context,
            "execution_status": "FAIL" # Set initial status, assuming user code is failing
        }
    
    except Exception as e:
        print(f"ERROR in Ingestor Node: {e}")
        return {
            "execution_status": "ERROR",
            "final_response": f"❌ Error retrieving problem from URL: {e}"
        }

# ---