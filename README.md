
## Title: HintForge: Intelligent Socratic Coding Tutor

## Overview

HintForge is an intelligent agentic workflow designed to assist competitive programmers without revealing full solutions. Instead of acting as a code generator, HintForge functions as a **Socratic Tutor**. It accepts a problem statement (URL or text) along with the user's failing code (e.g., TLE, Wrong Answer) as input.

The agent uses a multi-node LangGraph workflow to:

1. **Ingest** problem statements from URLs using Tavily API, extracting and cleaning unstructured HTML content into usable context.

2. **Analyze** the problem constraints and evaluate the time complexity of the user's code, diagnosing logical or performance failures.

3. **Generate** a counter-example test case that breaks the user's current solution, helping them understand where their approach fails.

4. **Tutor** by producing progressive, structured hints that guide the user without providing direct code solutions.

5. **Critique & Reflect** through an internal feedback loop that ensures hints are neither too vague nor too spoiler-y, refining the output until it meets pedagogical standards.

6. **Suggest Resources** (via Streamlit UI) by recommending high-quality tutorials and learning materials based on the detected algorithmic concepts.


## Reason for Picking Up This Project

This project aligns perfectly with advanced AI agent development concepts, integrating every major technique in modern LLM orchestration:

1. **LangGraph & State Management**
   - HintForge implements a structured **StateGraph** with multiple interconnected nodes (Ingestor, Analyzer, Hacker, Tutor, Critic, Router) for analysis, retrieval, and hint generation.
   - State transitions ensure smooth data flow across the agent pipeline, with conditional edges enabling reflection loops.

2. **RAG & Semantic Search**
   - Performs **Retrieval-Augmented Generation** by loading unstructured problem statements directly from URLs using Tavily Search API.
   - The Ingestor node scrapes and processes HTML content, converting it into clean text context for downstream analysis.

3. **Tool Calling & External APIs**
   - The agent autonomously calls external tools such as **Tavily Search** to fetch problem statements and (in the Streamlit UI) to find relevant learning resources.
   - Dynamically generates search queries based on detected algorithmic needs and problem context.

4. **Structured Output**
   - Enforces strict **Pydantic-based JSON schemas** for hint generation (the `Hint` model in `graph_state.py`), ensuring clarity, consistency, and pedagogical structure instead of free-form LLM text.
   - Uses LangChain's `with_structured_output()` to guarantee valid, type-safe responses.

5. **Reflection & Self-Correction**
   - Implements a **critic-reflect loop** where the Critic node reviews hints and can request regeneration, demonstrating self-improving agent behavior.

6. **Multi-Model Orchestration**
   - Strategically uses different GPT models (GPT-4o for complex test case generation, GPT-4o-mini for analysis and tutoring) to balance cost and quality.


## Video Summary Link: 



### Plan

I planned to execute these steps to complete the HintForge project:

- [DONE] **Step 1**: Set up project structure, virtual environment, and install core dependencies (LangGraph, LangChain, OpenAI, Tavily, Pydantic)

- [DONE] **Step 2**: Define the `GraphState` TypedDict and `Hint` Pydantic model in `graph_state.py` to establish the shared state schema and structured output format

- [DONE] **Step 3**: Implement the **Ingestor Node** (`ingestor_node.py`) with Tavily API integration to fetch and parse problem statements from URLs

- [DONE] **Step 4**: Implement the **Analyzer Node** (`analyzer_node.py`) using GPT-4o-mini to diagnose code flaws and identify required time complexity

- [DONE] **Step 5**: Implement the **Hacker Node** (`hacker_node.py`) using GPT-4o to generate counter-example test cases that break the user's solution

- [DONE] **Step 6**: Implement the **Tutor Node** (`tutor_node.py`) with structured output (Pydantic) to generate non-spoiler Socratic hints

- [DONE] **Step 7**: Implement the **Critic Node** (`critic_node.py`) to review hint quality and provide feedback for regeneration

- [TODO] **Step 8**: Implement the **Router Function** (`router_function.py`) with conditional edge logic to manage the reflection loop

- [TODO] **Step 9**: Build the main LangGraph workflow in `hintforge_agent.py`, connecting all nodes with proper edges and conditional routing

- [TODO] **Step 10**: Create the Streamlit web UI (`app.py`) for user-friendly interaction with the agent

- [TODO] **Step 11**: Add learning resources suggestion feature in the Streamlit UI that recommends tutorials based on detected algorithmic concepts

- [TODO] **Step 12**: Write comprehensive README documentation covering architecture, file structure, setup instructions, and usage


### Conclusion 



  
