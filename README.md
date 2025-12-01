

## Title: HintForge: An Intelligent Code Analysis Agent for Competitive Programming

## Overview
HintForge is a LangGraph-powered intelligent tutoring agent for Competitive Programming that avoids the “Spoiler Problem.” Instead of revealing full solutions, it analyzes the problem statement (URL/text) and the user’s failing code to guide learning.
It detects time-complexity issues, extracts constraints, and identifies the missing algorithm (e.g., Binary Search, DP, Fenwick Tree).
HintForge then performs web search via Tavily to retrieve high-quality tutorials.
Finally, it generates a structured, Socratic hint that nudges the user toward the correct approach without giving code.
By combining RAG, tool-calling, structured output, and LangGraph’s multi-node workflow, HintForge provides an editorial-free, guided learning experience that builds real problem-solving skills.

## Reason for picking up this project
Reason for picking up this project
I selected this project because it perfectly demonstrates the power of Agentic Workflows in education. It covers all major course topics:

**RAG**: The agent must ingest and "understand" the unstructured text of the problem statement and constraints.

**Tool Calling**: It utilizes web search tools to dynamically fetch learning resources, ensuring the advice is not limited to the LLM's training data.

**LangGraph**: The application relies on state management to pass data between the "Logic Analyzer" node and the "Researcher" node.

**Structured Output**: The final response is constrained to a strict format (Hint + Link + Explanation) rather than free-form chat.

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




  
