import os
import asyncio
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.mcp import McpToolSpec
from llama_index.core import Settings
from mcp import ClientSession
from mcp.client.sse import sse_client

Settings.llm = OpenAI(
    model="gpt-3.5-turbo",
    api_base="http://localhost:1234/v1",
    api_key="lm-studio",
    is_chat_model=True,
    temperature=0.7
)
Settings.embed_model = "local:BAAI/bge-small-en-v1.5"

async def main():
    print("🔌 Connecting to MCP server and creating agent...")

    # Create an SSE client connection to the MCP server
    async with sse_client(url="http://localhost:8001/sse") as streams:
        async with ClientSession(*streams) as session:
            # Initialize the session
            await session.initialize()

            # Create McpToolSpec with the client session
            mcp_tool_spec = McpToolSpec(session)

            # Convert the spec into a list of tools the agent can use
            mcp_tools = await mcp_tool_spec.to_tool_list_async()

            print(f"✅ Discovered {len(mcp_tools)} tool(s):")
            for tool in mcp_tools:
                print(f"- {tool.metadata.name}: {tool.metadata.description}")

            # Create a LlamaIndex agent with these tools using LM Studio
            agent = ReActAgent(tools=mcp_tools, llm=Settings.llm, verbose=True)

            print("\n🤖 Agent is ready! Ask it to use the document tool.")

            # Interact with the agent using the workflow-based run method
            response = await agent.run(user_msg="Can you get me the information for document ID 42?")
            print("\nAgent's Final Response:")
            print(response)

if __name__ == "__main__":
    asyncio.run(main())
