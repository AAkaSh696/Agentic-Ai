import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


async def main():
    # This brings all tools from MCP servers
    client = MultiServerMCPClient({
        "docker-mcp": {
            "transport": "stdio",
            "command": "python.exe",
            "args": ["03_mcp_server.py"]
        }
    })

    tools = await client.get_tools()

    llm = ChatOllama(model="qwen2.5:3b", temperature=0)

    agent = create_agent(llm, tools)

    print("\nDocker AI Agent Started!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Agent stopped.")
            break

        if not user_input:
            continue

        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_input}]
        })

        print("\nAgent:", response["messages"][-1].content, "\n")


if __name__ == "__main__":
    asyncio.run(main())