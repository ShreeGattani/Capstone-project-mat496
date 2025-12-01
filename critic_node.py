import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Annotated, Literal
from graph_state import GraphState 

# --- Model Initialization ---
# Using a precise model for structured decision-making (critique)
llm_critic = ChatOpenAI(model="gpt-4o-mini", temperature=0.0) 

# --- Critic Node Prompt ---
critic_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         "You are the **Critic Node** for Hintforge. Your job is to rigorously review the generated hint. "
         "You must decide if the hint is acceptable or if it needs to be regenerated. "
         "The goal is to provide a hint that is GUIDING but NON-SPOILER."
         "\n\n---Review Criteria---"
         "\n1. SPOILER CHECK: Does the hint explicitly or implicitly reveal the fix, an exact line of code, or the full algorithm name/formula? (e.g., 'Use two pointers', 'Sort the array', 'The DP transition is X')."
         "\n2. VAGUENESS CHECK: Is the hint too generic or unhelpful? (e.g., 'Check your logic', 'Rethink the problem')."
         "\n\n---Problem Context---\n{problem_context}"
         "\n\n---Failing User Code---\n{user_code}"
         "\n\n---Tutor's Generated Hint (Analysis: {analysis})---\n{socratic_hint}"
         ),
        
        ("human", 
         "Review the hint against the criteria. If the hint is **acceptable**, respond with a single word: 'ACCEPT'. "
         "If the hint is **unacceptable** (too much of a spoiler or too vague), respond with the word 'REGENERATE' followed by a brief, actionable reason for the Tutor to improve the hint (e.g., 'REGENERATE: The hint mentions the exact data structure needed. Reword it to focus on complexity.')"
         "Your full response must be one of the two formats: 'ACCEPT' or 'REGENERATE: [Reason]'.")
    ]
)

# --- Critic Node Function ---
def critique_hint(state: GraphState) -> GraphState:
    """
    Reviews the current hint and decides whether to accept it or force regeneration.
    
    Args:
        state (GraphState): The current state of the graph.
        
    Returns:
        GraphState: The updated state with the reflection decision (or an error).
    """
    print("---CRITIC NODE: Reviewing Hint---")
    
    if state.get("execution_status") == "ERROR" or state.get("current_hint") is None:
        print("Skipping critique due to error or missing hint.")
        return state

    critic_chain = critic_prompt | llm_critic
    hint = state["current_hint"]
    
    try:
        response = critic_chain.invoke(
            {
                "problem_context": state["problem_context"],
                "user_code": state["user_code"],
                "analysis": hint.analysis,
                "socratic_hint": hint.socratic_hint
            }
        ).content.strip()
        
        # Parse the decision and feedback
        if response.startswith("ACCEPT"):
            print("Critique: ACCEPTED.")
            return {
                "feedback": None,
                "final_response": "ACCEPTED" # Sentinel value for the conditional edge
            }
        else:
            # Assumes format is 'REGENERATE: [Reason]'
            feedback = response.replace("REGENERATE:", "").strip()
            print(f"Critique: REGENERATE. Reason: {feedback}")
            return {
                "feedback": feedback,
                "final_response": "REGENERATE" # Sentinel value for the conditional edge
            }

    except Exception as e:
        print(f"ERROR in Critic Node: {e}")
        return {
            "execution_status": "ERROR",
            "final_response": f"❌ Error during critique: {e}"
        }

# ---