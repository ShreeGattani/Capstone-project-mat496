import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Annotated
from graph_state import GraphState, Hint  # Import the Hint schema

# --- Model Initialization ---
# Using a standard model for text generation with structured Pydantic output
base_llm_tutor = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
# Let LangChain / OpenAI handle structured output tool-calling into the Hint model
llm_tutor = base_llm_tutor.with_structured_output(Hint)

# --- Tutor Node Prompt ---
tutor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are the **Socratic Tutor** for Hintforge. Your goal is to guide the student "
            "towards the correct solution without giving away the answer (NO SPOILERS).\n\n"
            "Given the problem context, the student's failing code, the internal diagnosis of "
            "the flaw, and a counter-example input, you must produce a structured hint that "
            "matches the Hint schema (fields: analysis, counter_example_input, socratic_hint, "
            "complexity_advice)."
        ),
        (
            "human",
            "Use the following information to fill in the Hint fields:\n\n"
            "---Problem Context---\n{problem_context}\n\n"
            "---Failing User Code ({language})---\n{user_code}\n\n"
            "---Internal Diagnosis---\n{execution_output}\n\n"
            "---Generated Counter-Example---\n{generated_test_case}\n\n"
            "---Critique Feedback (if regenerating)---\n{feedback}\n\n"
            "Return a helpful, non-spoiler hint."
        ),
    ]
)

# --- Tutor Node Function ---
def generate_socratic_hint(state: GraphState) -> GraphState:
    """
    Generates a structured Socratic hint and populates the current_hint field.
    
    Args:
        state (GraphState): The current state of the graph.
        
    Returns:
        GraphState: The updated state with the current_hint.
    """
    print("---TUTOR NODE: Generating Socratic Hint---")
    
    if state.get("execution_status") == "ERROR":
        print("Skipping hint generation due to previous error.")
        return state
    # Chain prompt -> structured LLM (returns a Hint instance)
    tutor_chain = tutor_prompt | llm_tutor
    
    try:
        # Prepare inputs, ensuring 'feedback' is handled (will be None on the first pass)
        inputs = {
            "problem_context": state["problem_context"],
            "user_code": state["user_code"],
            "language": state["language"],
            "execution_output": state["execution_output"],
            "generated_test_case": state["generated_test_case"],
            "feedback": state.get("feedback", "No prior feedback.")
        }
        
        # Invoke the chain, which returns a Hint Pydantic model
        hint_model: Hint = tutor_chain.invoke(inputs)
        
        print(f"Initial Hint Generated (Analysis: {hint_model.analysis})")
        
        # Increment reflection count for tracking
        reflection_count = state.get("reflection_count", 0) + 1
        
        return {
            "current_hint": hint_model,
            "reflection_count": reflection_count,
            # Reset feedback for the next loop (if any)
            "feedback": None
        }
        
    except Exception as e:
        print(f"ERROR in Tutor Node: {e}")
        return {
            "execution_status": "ERROR",
            "final_response": f"❌ Error during hint generation: {e}"
        }

# ---