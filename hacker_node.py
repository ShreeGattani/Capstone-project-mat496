import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Annotated
from graph_state import GraphState 

# --- Model Initialization ---
# Using a powerful model to reliably generate complex test cases
llm_hacker = ChatOpenAI(model="gpt-4o-mini", temperature=0.3) 

# --- Hacker Node Prompt ---
hacker_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are the **Hacker Node** for Hintforge. Your job is to generate a single, minimal, "
         "highly effective test case that exploits the logical flaw described in the 'Internal Analysis'. "
         "The test case must be valid according to the problem constraints."
         "\n\n---Problem Context---\n{problem_context}"
         "\n\n---Failing User Code ({language})---\n{user_code}"
         "\n\n---Internal Analysis of Flaw (Type: {execution_output})---\n"
         "Your generated test case will be run against this user code to confirm the failure."),
        
        ("human", 
         "Based on the analysis, generate ONLY the raw input data (the test case) that would cause the user's code to fail. "
         "Do not include any explanation, headers, or surrounding text, just the required input data formatted exactly as expected by the problem statement.")
    ]
)

# --- Hacker Node Function ---
def generate_test_case(state: GraphState) -> GraphState:
    """
    Generates a high-impact counter-example that breaks the user's logic.
    
    Args:
        state (GraphState): The current state of the graph.
        
    Returns:
        GraphState: The updated state with the generated_test_case.
    """
    print("---HACKER NODE: Generating Counter-Example---")
    
    if state.get("execution_status") == "ERROR":
        print("Skipping test case generation due to previous error.")
        return state

    hacker_chain = hacker_prompt | llm_hacker
    
    try:
        # Invoke the LLM to generate the raw test case input
        response = hacker_chain.invoke(
            {
                "problem_context": state["problem_context"],
                "user_code": state["user_code"],
                "language": state["language"],
                "execution_output": state.get("execution_output", "Undetermined flaw.")
            }
        )
        
        test_case = response.content.strip()
        print(f"Generated Test Case: \n{test_case[:50]}...") # Show a snippet
        
        # NOTE: In a real system, we would execute the user_code here with 'test_case'
        # and confirm it fails. For this prototype, we assume it's valid.
        
        return {
            "generated_test_case": test_case,
            # We skip actual execution and move straight to tutoring for the prototype
            "execution_status": "FAIL", 
        }
        
    except Exception as e:
        print(f"ERROR in Hacker Node: {e}")
        return {
            "execution_status": "ERROR",
            "final_response": f"❌ Error during test case generation: {e}"
        }

# ---