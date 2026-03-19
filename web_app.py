import io
from contextlib import redirect_stdout

import streamlit as st
from crewai import Crew
from dotenv import load_dotenv

from agents.coding_agent import create_coding_agent
from agents.explanation_agent import create_explanation_agent
from agents.research_agent import create_research_agent
from agents.review_agent import create_review_agent
from main import build_llm
from tasks.tasks import create_tasks


load_dotenv(override=True)


def _format_task_output(task) -> str:
    output = getattr(task, "output", None)
    if output is None:
        return "No output captured for this task."

    raw_output = getattr(output, "raw", None)
    if raw_output:
        return str(raw_output)

    return str(output)


def run_crew_request(user_problem: str) -> dict:
    llm, provider = build_llm()
    if llm is None:
        return "LLM setup failed. Check your .env provider and API key."

    research_agent = create_research_agent(llm)
    coding_agent = create_coding_agent(llm)
    review_agent = create_review_agent(llm)
    explanation_agent = create_explanation_agent(llm)

    tasks = create_tasks(
        research_agent,
        coding_agent,
        review_agent,
        explanation_agent,
        user_problem,
    )

    crew = Crew(
        agents=[research_agent, coding_agent, review_agent, explanation_agent],
        tasks=tasks,
        verbose=True,
    )

    terminal_buffer = io.StringIO()

    try:
        with redirect_stdout(terminal_buffer):
            result = crew.kickoff()

        task_results = []
        for index, task in enumerate(tasks, start=1):
            role = getattr(getattr(task, "agent", None), "role", f"Agent {index}")
            task_results.append(
                {
                    "index": index,
                    "role": role,
                    "description": getattr(task, "description", ""),
                    "output": _format_task_output(task),
                }
            )

        return {
            "ok": True,
            "final_output": str(result),
            "task_results": task_results,
            "terminal_logs": terminal_buffer.getvalue().strip(),
        }
    except Exception as exc:
        error_text = str(exc).lower()
        if "insufficient_quota" in error_text or "exceeded your current quota" in error_text:
            return {
                "ok": False,
                "error": f"{provider} quota exceeded. Add billing/credits and try again.",
                "terminal_logs": terminal_buffer.getvalue().strip(),
            }
        if "invalid_api_key" in error_text or "incorrect api key" in error_text or "401" in error_text:
            return {
                "ok": False,
                "error": f"Invalid {provider} API key. Update .env and retry.",
                "terminal_logs": terminal_buffer.getvalue().strip(),
            }
        return {
            "ok": False,
            "error": f"Unexpected error: {exc}",
            "terminal_logs": terminal_buffer.getvalue().strip(),
        }


def main() -> None:
    st.set_page_config(page_title="MultiAgentLLM", page_icon="AI", layout="wide")
    st.title("MultiAgentLLM Browser App")
    st.write("Enter your problem and run the multi-agent workflow from your browser.")

    user_problem = st.text_area(
        "Your problem/request",
        placeholder="Example: Build a Python function to validate email addresses.",
        height=180,
    )

    run_clicked = st.button("Run Agents", type="primary")

    if run_clicked:
        if not user_problem.strip():
            st.error("Please enter a valid problem statement.")
            return

        with st.spinner("Running agents, please wait..."):
            result = run_crew_request(user_problem.strip())

        if not result.get("ok"):
            st.error(result.get("error", "Something went wrong."))
            if result.get("terminal_logs"):
                st.subheader("Terminal Logs")
                st.code(result["terminal_logs"], language="text")
            return

        st.subheader("Agent Execution")
        for item in result.get("task_results", []):
            with st.expander(f"Step {item['index']}: {item['role']}", expanded=True):
                st.write(item["description"])
                st.code(item["output"], language="text")

        logs = result.get("terminal_logs", "")
        if logs:
            st.subheader("Terminal Logs")
            st.code(logs, language="text")

        st.subheader("Final Output")
        st.code(result.get("final_output", ""), language="text")


if __name__ == "__main__":
    main()
