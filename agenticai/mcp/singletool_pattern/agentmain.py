import asyncio
import base64
from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec


def setup_llm():
    """
    Configure Azure OpenAI (reusable config)
    """
    client_key = "myclientid"
    client_secret = "mysecretpassword"
    id_secret_bytes = client_key + ":" + client_secret
    tokenID = base64.b64encode(id_secret_bytes.encode()).decode()
    openai_api_base = "https://myapi.openai.azure.com/"

    Settings.llm = AzureOpenAI(
        model="gpt-4o",
        engine="gpt-4o-20240513-global",
        azure_endpoint=openai_api_base,
        api_version="2024-12-01-preview",
        api_key=tokenID,
        temperature=0.0,
        max_retries=5,
    )

    Settings.embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="text-embedding-ada-002",
        azure_endpoint=openai_api_base,
        api_version="2024-10-21",
        api_key=tokenID,
        max_retries=5,
    )


async def run_example(
    agent: ReActAgent, example_name: str, prompt: str, max_iterations: int = 30
):
    """Helper function to run an example and display results."""
    print(f"\n{'='*80}")
    print(f"🧪 EXAMPLE: {example_name}")
    print(f"{'='*80}")
    print(f"📝 Prompt: {prompt}\n")

    handler = agent.run(prompt, max_iterations=max_iterations)
    response = await handler

    print(f"\n✅ Response:\n{response}\n")
    return response


async def main():

    setup_llm()
    client = BasicMCPClient(command_or_url="http://127.0.0.1:8000/mcp")

    print("🔌 Connecting to Synthetic User Factory...")
    try:
        tool_spec = McpToolSpec(client=client)
        mcp_tools = await tool_spec.to_tool_list_async()
        print(f"✅ Connected! Available tools: {len(mcp_tools)}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    agent = ReActAgent(tools=mcp_tools, verbose=True)

    # Example 1: Validate locales before generation
    await run_example(
        agent,
        "Validate Locales",
        "Before generating data, please VALIDATE if these locales are supported: "
        "es_ES (Spain), ja_JP (Japan), and fr_FR (France).",
    )

    # Example 2: Preview samples from multiple locales
    await run_example(
        agent,
        "Preview Samples",
        "Show me a PREVIEW of what user data looks like for: "
        "1. Italy (it_IT) with address and company details "
        "2. Germany (de_DE) with just basic info. "
        "Just one sample per locale.",
    )

    # Example 3: Count total users
    await run_example(
        agent,
        "Count Total Users",
        "Tell me how many total users would be generated if I request: "
        "5 users from Brazil (pt_BR), 10 from India (en_IN), and 3 from Mexico (es_MX).",
    )

    # Example 4: Full generation with composite batches
    await run_example(
        agent,
        "Generate Multi-Locale Dataset",
        "GENERATE a dataset with: "
        "3 users from Spain (es_ES) with addresses and phones, "
        "2 users from Japan (ja_JP) with names, emails, and company details, "
        "1 user from France (fr_FR) with complete information. "
        "Use seed 42.",
    )

    # Example 5: Complex multi-step workflow
    await run_example(
        agent,
        "Multi-Step Workflow",
        "Execute these operations in ONE tool call: validate, count, and generate for locales en_US, zh_CN, and ar_SA. "
        "Generate 10 users from each locale with addresses included.",
        max_iterations=25,
    )

    print(f"\n{'='*80}")
    print("🎉 All examples completed!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    asyncio.run(main())
