from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.agent import run_agent
import streamlit as st

from src.agent import run_agent


st.set_page_config(
    page_title="Developer Assistant",
    page_icon="🧠",
    layout="wide",
)


def render_list(title: str, items):
    st.subheader(title)

    if not items:
        st.write("None.")
        return

    for item in items:
        st.markdown(f"- {item}")


def render_potential_bugs(potential_bugs):
    st.subheader("Potential Bugs")

    if not potential_bugs:
        st.success("No potential bugs found.")
        return

    for bug in potential_bugs:
        with st.expander(bug.bug):
            st.write(bug.explanation)

            if hasattr(bug, "severity"):
                st.write(f"Severity: {bug.severity}")


def render_tools_used(tools_used):
    st.subheader("Tools Used")

    if not tools_used:
        st.write("No tools used.")
        return

    for tool in tools_used:
        if isinstance(tool, str):
            st.markdown(f"- `{tool}`")
        else:
            tool_name = getattr(tool, "tool_name", "Unknown tool")
            reason = getattr(tool, "reason", "")

            st.markdown(f"- `{tool_name}`")
            if reason:
                st.caption(reason)


st.title("Developer Assistant")
st.write("Analyze developer requests, code, bugs, and feature ideas using your agent.")

with st.sidebar:
    st.header("About")
    st.write(
        "This interface calls the same `run_agent()` function "
        "used by your CLI app."
    )

    st.divider()

    st.write("Suggested tests:")
    st.code(
        """def hello(
    print("hi")""",
        language="python",
    )


with st.form("developer_assistant_form"):
    user_request = st.text_area(
        "What do you want help with?",
        placeholder="Example: Check this code and explain the bug.",
        height=120,
    )

    code_context = st.text_area(
        "Paste code/context if you have any",
        placeholder="Paste Python code, traceback, or project context here...",
        height=260,
    )

    submitted = st.form_submit_button("Analyze")


if submitted:
    if not user_request.strip():
        st.warning("Please write a developer request first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                report = run_agent(
                    user_request=user_request,
                    code_context=code_context,
                )
            except Exception as e:
                st.error("The developer assistant failed.")
                st.exception(e)
                st.stop()

        st.success("Analysis complete.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Task Type", report.task_type)

        with col2:
            st.metric("Difficulty", report.difficulty)

        with col3:
            st.metric("Risk Level", report.risk_level)

        st.subheader("Summary")
        st.write(report.summary)

        render_list("Key Points", report.key_points)

        render_potential_bugs(report.potential_bugs)

        render_list("Next Steps", report.next_steps)

        st.subheader("Needs Human Review")
        if report.needs_human_review:
            st.warning("Yes")
        else:
            st.success("No")

        if hasattr(report, "tools_used"):
            render_tools_used(report.tools_used)

        with st.expander("Raw Structured Output"):
            st.json(report.model_dump())