import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Annotated
from graph_state import GraphState 

# Load environment variables from .env (if present) before initializing the LLM
load_dotenv()

# --- Model Initialization ---
# Using a powerful model for complex logic analysis
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1) 

# --- Logic Analyzer Prompt ---
analyzer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are the **Logic Analyzer** for Hintforge. Your job is to analyze the user's "
         "failing code against the problem statement. You must identify the root logical "
         "error and the *correct* algorithmic complexity required. DO NOT give the fix. "
         "Focus on the flaw's *type* (e.g., greedy choice failed, incorrect DP state, O(N^2) time limit exceeded)."
         "\n\n---Problem Context---\n{problem_context}\n\n---Failing User Code ({language})---\n{user_code}"),
        
        ("human", 
         "Analyze the user's solution. State the likely reason it fails (e.g., Time Limit Exceeded, Wrong Answer, specific logic bug) "
         "and the target complexity needed to pass (e.g., O(N log N) or O(N)). "
         "Provide a concise, internal-only summary. Do not use Markdown formatting.")
    ]
)

# --- Logic Analyzer Node Function ---
def analyze_logic(state: GraphState) -> GraphState:
    """
    Analyzes the user's code against the problem context to determine the root cause 
    and target complexity. This output is for internal use by the Hacker/Tutor.
    
    Args:
        state (GraphState): The current state of the graph.
        
    Returns:
        GraphState: The updated state with the execution_output (internal analysis).
    """
    print("---LOGIC ANALYZER NODE: Diagnosing Flaw---")
    
    if state.get("execution_status") == "ERROR":
        print("Skipping analysis due to previous ingestion error.")
        return state

    analysis_chain = analyzer_prompt | llm
    
    try:
        # Invoke the LLM to get the internal diagnostic summary
        response = analysis_chain.invoke(
            {
                "problem_context": state["problem_context"],
                "user_code": state["user_code"],
                "language": state["language"]
            }
        )
        
        print(f"Internal Analysis Complete.")
        
        # Store the internal analysis in 'execution_output' 
        return {
            "execution_output": response.content,
            # Execution status remains 'FAIL' as we haven't successfully tested the code yet.
        }
        
    except Exception as e:
        print(f"ERROR in Logic Analyzer Node: {e}")
        return {
            "execution_status": "ERROR",
            "final_response": f"❌ Error during AI logic analysis: {e}"
        }

# ---