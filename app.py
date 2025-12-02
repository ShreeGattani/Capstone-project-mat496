import os

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from hintforge_agent import build_hintforge_graph

@st.cache_resource
def get_app():
    """Build and cache the LangGraph app so it is reused across reruns."""
    load_dotenv()
    return build_hintforge_graph()


def run_hintforge(problem_url: str, user_code: str, language: str = "C++"):
    """Helper to invoke the graph with user-provided inputs."""
    app = get_app()
    initial_state = {
        "problem_url": problem_url,
        "user_code": user_code,
        "language": language,
        "reflection_count": 0,
    }
    return app.invoke(initial_state)


def suggest_learning_resources(analysis: str, language: str) -> list[str]:
    """
    Ask the LLM for a few high‑quality learning resources (links)
    related to the error / concept in the analysis.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return []

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    prompt = (
        "You are a tutoring assistant helping a competitive programming student.\n"
        "Based on the following analysis of their mistake, suggest 3–5 high‑quality "
        "online resources (tutorials, blog posts, video series, or documentation) "
        "that they can follow to learn the relevant concepts.\n\n"
        f"Language: {language}\n"
        f"Analysis: {analysis}\n\n"
        "Return each resource on its own line in the form 'Title — URL'. "
        "Only include reputable, broadly useful resources (not random paste sites)."
    )

    try:
        resp = llm.invoke(prompt)
        lines = [ln.strip() for ln in resp.content.splitlines() if ln.strip()]
        return lines[:5]
    except Exception:
        return []


def main():
    st.set_page_config(page_title="Hintforge", page_icon="💡", layout="wide")

    st.title("Hintforge – Competitive Programming Hint Agent")
    st.write(
        "Paste a problem URL and your (currently failing) solution. "
        "Hintforge will analyze it, generate a counter-example, and return a non‑spoiler hint."
    )

    

    with st.sidebar:
        st.header("Problem & Language")
        problem_url = st.text_input(
            "Problem URL",
            value="",
        )
        language = st.selectbox("Language", ["C++", "Python", "Java"], index=0)

        st.markdown("**Environment**")
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        has_tavily = bool(os.getenv("TAVILY_API_KEY"))
        st.write(f"OPENAI_API_KEY set: {'✅' if has_openai else '❌'}")
        st.write(f"TAVILY_API_KEY set: {'✅' if has_tavily else '❌'}")

    default_code = """
"""

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Code")
        user_code = st.text_area(
            "Paste your solution here",
            value=default_code,
            height=350,
        )
        run_button = st.button("Run ", type="primary")

    with col2:
        st.subheader("Output")
        output_placeholder = st.empty()

    if run_button:
        if not problem_url.strip():
            st.error("Please provide a problem URL.")
            return
        if not user_code.strip():
            st.error("Please paste your code.")
            return
        if not os.getenv("OPENAI_API_KEY"):
            st.error("OPENAI_API_KEY is not set. Add it to your .env file.")
            return

        with st.spinner("Running agent... this may take a few seconds."):
            try:
                final_state = run_hintforge(problem_url.strip(), user_code, language)
            except Exception as e:
                st.error(f"FATAL ERROR DURING EXECUTION: {e}")
                return

        exec_status = final_state.get("execution_status")
        final_hint = final_state.get("current_hint")
        final_error = final_state.get("final_response")

        with output_placeholder.container():
            if final_hint is not None:
                st.success(
                    f"Reflection Complete "
                    f"in {final_state.get('reflection_count', 1)} passes."
                )

                st.markdown("### Counter-example input")
                st.code(final_hint.counter_example_input, language="")

                st.markdown("### Analysis")
                st.write(final_hint.analysis)

                st.markdown("### Socratic hint")
                st.write(final_hint.socratic_hint)

                if final_hint.complexity_advice:
                    st.markdown("### Complexity advice")
                    st.write(final_hint.complexity_advice)

                resources = suggest_learning_resources(final_hint.analysis, language)
                if resources:
                    st.markdown("### Suggested tutorials & learning resources")
                    for r in resources:
                        st.write(f"- {r}")

            elif exec_status == "ERROR":
                st.error(final_error or "Process ended with an unknown error.")
            else:
                st.warning("Process ended without producing a hint.")


if __name__ == "__main__":
    main()


