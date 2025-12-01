
## Title: HintForge: Intelligent Socratic Coding Tutor

## Overview

HintForge is an intelligent agentic workflow designed to assist competitive programmers without revealing full solutions. Instead of acting as a code generator, HintForge functions as a "Socratic Tutor." It accepts a problem statement (URL or text) along with the user's failing code (e.g., TLE, Wrong Answer) as input.

The agent uses a multi-node LangGraph workflow to:
1. **Analyze** the problem constraints and evaluate the time complexity of the user's code.
2. **Diagnose** logical or performance failures based on extracted problem constraints.
3. **Research** the required algorithm using external web tools to find high-quality tutorials.
4. **Generate** a progressive, structured hint that guides the user without providing direct code.

## Reason for picking up this project
This project aligns perfectly with the MAT496 curriculum, integrating every major concept taught in the course:

1. **LangGraph:**  - HintForge implements a structured **StateGraph** with multiple interconnected nodes for analysis, retrieval, and hint generation. State transitions ensure smooth data flow across the agent pipeline.

2. **RAG & Semantic Search:**  - It performs Retrieval-Augmented Generation by loading unstructured problem statements directly from URLs and searching the web for algorithmic explanations using semantic search tools.

3. **Tool Calling:**  - The agent autonomously calls external tools such as **Tavily Search** to fetch relevant learning resources, dynamically generating search queries based on detected algorithmic needs.

4. **Structured Output:**  - It enforces strict Pydantic-based JSON schemas for hint generation, ensuring clarity, consistency, and pedagogical structure instead of free-form LLM text.

## Video Summary Link: 



## Plan

I plan to execute these steps to complete my project.

- [TODO] Step 1 involves blah blah
- [TODO] Step 2 involves blah blah
- [TODO] Step 3 involves blah blah
- ...
- [TODO] Step n involves blah blah

## Conclusion:

I had planned to achieve {this this}. I think I have/have-not achieved the conclusion satisfactorily. The reason for your satisfaction/unsatisfaction.




  
