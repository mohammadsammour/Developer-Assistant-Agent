from langchain.agents import create_agent
from src.config import load_model
from src.schemas import DeveloperTaskReport
from src.tools import developer_tools
from src.prompts import DEVELOPER_AGENT_SYSTEM_PROMPT, build_developer_user_message

def build_analysis_agent():
    llm = load_model()
    agent = create_agent(
        model= llm,
        system_prompt= DEVELOPER_AGENT_SYSTEM_PROMPT,
        tools = developer_tools,
        response_format=DeveloperTaskReport
    )
    return agent

def run_agent(user_request : str, code_context : str) -> DeveloperTaskReport:
    agent = build_analysis_agent()
    user_message = build_developer_user_message(user_request,code_context)
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_message}
        ]
    })

    report = result.get("structured_response")

    if report is None:
        print("\n--- RAW AGENT RESULT DEBUG ---")
        print(result)
        print("--- END DEBUG ---\n")

        raise RuntimeError("Agent did not return a structured DeveloperTaskReport.")

    return report
