from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain.agents import create_agent
import subprocess

SYSTEM_PROMPT = """
You are Docker Expert. Answer in 1-2 lines max. Don't overthink or loop.
Always use the tools to get real data, never guess.

For any problem, tell:
1) The error (what went wrong)
2) The likely root cause
3) A short fix
"""

@tool
def show_running_containers() -> str:
    """Show all currently running Docker containers."""
    result = subprocess.run(
        ["docker", "ps"],
        capture_output=True,
        text=True,
    )
    return result.stdout or result.stderr or "No running containers."


@tool
def show_container_logs_by_name(container_name: str) -> str:
    """Show the last 50 log lines of a Docker container using its name."""
    result = subprocess.run(
        ["docker", "logs", "--tail", "50", container_name],
        capture_output=True,
        text=True,
    )
    return (result.stdout + result.stderr) or "No logs found."


llm = ChatOllama(model="qwen2.5:3b", temperature=0) # temperature == randomness
tools = [show_running_containers, show_container_logs_by_name]

agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT) # create agent with system promt

while True:
    user_input = input("Enter your prompt/message:\n")

    if user_input == "exit":
        break

    response = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })

    print(response["messages"][-1].content)