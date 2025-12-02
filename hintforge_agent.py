
import os
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, END
from typing import Literal
from graph_state import GraphState # Contains GraphState and Hint schemas
from ingestor_node import ingest_problem_context
from analyzer_node import analyze_logic
from hacker_node import generate_test_case
from tutor_node import generate_socratic_hint
from critic_node import critique_hint
from router_function import route_to_reflection

# Load environment variables from a local .env file (if present)


def build_hintforge_graph():
    """Builds and compiles the Hintforge LangGraph."""
    
    # 1. Define the Graph and the State
    workflow = StateGraph(GraphState)

    # 2. Define the Nodes (Computational Steps)
    workflow.add_node("ingest", ingest_problem_context)
    workflow.add_node("analyze", analyze_logic)
    workflow.add_node("hacker", generate_test_case)
    workflow.add_node("tutor", generate_socratic_hint)
    workflow.add_node("critic", critique_hint)

    # 3. Define the Edges (Sequential Flow)
    workflow.set_entry_point("ingest")
    workflow.add_edge("ingest", "analyze")
    workflow.add_edge("analyze", "hacker")
    workflow.add_edge("hacker", "tutor")
    workflow.add_edge("tutor", "critic")

    # 4. Define the Conditional Edge (The Reflection Loop)
    workflow.add_conditional_edges(
        # From the critic, route based on the result of the critique
        "critic",
        # Use the router function
        route_to_reflection,
        {
            # If the router returns 'regenerate', loop back to the Tutor
            "regenerate": "tutor",
            # If the router returns 'end', stop the execution
            "end": END
        }
    )

    # 5. Compile the Graph
    app = workflow.compile()
    
    return app

# --- Example Execution ---
if __name__ == "__main__":
    
    # IMPORTANT: Ensure your environment variables are set before running (e.g., OPENAI_API_KEY)

    # 1. Initialize the Graph
    hintforge_app = build_hintforge_graph()

    # 2. Define Initial State (Example Problem)
    # NOTE: This is a real-world URL for a famous competitive programming problem 
    # that often leads to an O(N^2) solution instead of the required O(N) or O(N log N).
    initial_state = {
        "problem_url": "https://codeforces.com/problemset/problem/1/A", # Placeholder: Use a real contest link for a proper test
        "user_code": """
            // User's failing C++ code snippet (e.g., O(N^2) solution for a O(N log N) problem)
            #include <iostream>
            #include <vector>
            using namespace std;
            
            int main() {
                int N;
                cin >> N;
                vector<int> a(N);
                for (int i = 0; i < N; ++i) {
                    cin >> a[i];
                }
                
                // Intentional O(N^2) flaw: simple nested loop sum check
                for (int i = 0; i < N; ++i) {
                    for (int j = i + 1; j < N; ++j) {
                        // Some calculation that should be done faster...
                        if (a[i] + a[j] > 1000) {
                            cout << "Found pair" << endl;
                            return 0;
                        }
                    }
                }
                cout << "Not found" << endl;
                return 0;
            }
            """,
        "language": "C++",
        "reflection_count": 0,
        # Other state variables are initialized to None/default by the nodes themselves
    }
    
    print("--- 🚀 STARTING HINTFORGE AGENT ---")
    
    # 3. Invoke the Graph
    try:
        # Stream the result for better visibility of the workflow
        for s in hintforge_app.stream(initial_state):
            print(s)
            print("-" * 20)

        # After streaming deltas, run once more to get the final full GraphState
        final_state = hintforge_app.invoke(initial_state)

        print("\n--- ✅ FINAL RESULT ---")
        # The final_state['current_hint'] is the validated, non-spoiler response (if present)
        final_hint = final_state.get("current_hint")
        exec_status = final_state.get("execution_status")
        final_msg = final_state.get("final_response")

        if final_hint is not None:
            # Treat presence of a Hint as success, even if execution_status is still "FAIL"
            print(f"\n✨ Hintforge Reflection Complete in {final_state.get('reflection_count', 1)} passes.")
            print("\n**YOUR COUNTER-EXAMPLE**")
            print(f"Input: \n{final_hint.counter_example_input}")
            print("\n**HINT FORGE TUTOR**")
            print(f"Analysis: {final_hint.analysis}")
            print(f"Hint: {final_hint.socratic_hint}")
            if final_hint.complexity_advice:
                print(f"Advice: {final_hint.complexity_advice}")
        elif exec_status == "ERROR":
            # Surface a meaningful error message if something went wrong
            print(f"Process ended with an error: {final_msg or 'Unknown Error'}")
        else:
            # No hint and no explicit ERROR status
            print("Process ended without producing a hint.")
            
    except Exception as e:
        print(f"\nFATAL ERROR DURING EXECUTION: {e}")

# ---