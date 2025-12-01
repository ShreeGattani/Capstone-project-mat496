from graph_state import GraphState

MAX_REFLECTIONS = 1

def route_to_reflection(state: GraphState) -> str:
    """
    Defines the conditional edge logic: should we loop back to the Tutor 
    for regeneration, or should we stop and output the final hint?
    """
    print("---ROUTER: Determining Next Step---")
    
    # 1. Handle Errors
    if state.get("execution_status") == "ERROR":
        return "end"
    
    # 2. Check for Acceptance
    if state.get("final_response") == "ACCEPTED":
        print("Route: Hint is approved. Finishing.")
        return "end"
    
    # 3. Check for Max Reflections
    if state.get("reflection_count", 0) >= MAX_REFLECTIONS:
        print("Route: Max reflections reached. Forcing output.")
        # If the critic keeps rejecting, we output the *best available* hint
        # and end the process to prevent infinite loops.
        return "end"

    # 4. Loop back for Regeneration
    print("Route: Hint needs refinement. Looping back to Tutor.")
    return "regenerate"

# ---