#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from fastmcp import FastMCP, Client
from fastmcp.server.auth.providers.jwt import JWTVerifier

APP_CONFIG = {"theme": "dark", "version": "1.1",
              "feature_flags": ["new_dashboard"]}

USER_PROFILES = {
    101: {"name": "Alice", "status": "active"},
    102: {"name": "Bob", "status": "inactive"},
}

# Use a static public key for token verification
PUBLIC_KEY_PEM = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArlL+Ll5ELidy1Q0cbgso
fApCyYF42r7a1y4PwTntjo9DT4LP6ixuoiLPPPTQP7HD3S531kfOskVczsFOkNkD
7wpTGWlPGvfmyJldqyRJg6T0SftcjznUOHpXZQu3U/kXKbRa8R2EdukKVBJcSdiG
cyPDkbkNUNJvEGyD/n+SgLRpsvDgLLdh7n25VeMM+q2BtVvpx4qLXrCXfahFG7Cd
elz7wJCNpKFlhfnzjPwoAKCQjyHVaZ1Ex9c2w0kRHT3qdn4fk8q4Rskobk08nZhj
Ep3gwUVCsjHfkbfC9Uo9hiJWbDgXgZOZFewmKagpKa9fANFDvpLQEYwCHi/qZvRx
ZwIDAQAB
-----END PUBLIC KEY-----
"""

verifier = JWTVerifier(
    public_key=PUBLIC_KEY_PEM,
    issuer="https://auth.example.com",
    audience="mcp-production-api"
)

mcp = FastMCP(name="Demo 🚀", auth=verifier)


@mcp.tool()
def greet(name: str) -> str:
    """Returns a simple greeting."""
    return f"Hello, {name}!"


@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b


@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return APP_CONFIG


@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: int) -> dict:
    """Retrieves a user's profile by their ID."""
    # The {user_id} from the URI is automatically passed as an argument
    return USER_PROFILES.get(user_id, {"error": "User not found"})


@mcp.prompt("summarize")
async def summarize_prompt(text: str) -> list[dict]:
    """Generates a prompt to summarize the provided text."""
    return [
        {"role": "system", "content": "You are a helpful assistant skilled at summarization."},
        {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
    ]


async def test_server_locally():
    print("\n--- Testing Server Locally ---")
    # Point the client directly at the server object
    client = Client(mcp)

    # Clients are asynchronous, so use an async context manager
    async with client:
        # Call the 'greet' tool
        greet_result = await client.call_tool("greet", {"name": "FastMCP User"})
        print(f"greet result: {greet_result}")

        # Call the 'add' tool
        add_result = await client.call_tool("add", {"a": 5, "b": 7})
        print(f"add result: {add_result}")

        # Read the 'config' resource
        config_data = await client.read_resource("data://config")
        print(f"config resource: {config_data}")

        # Read a user profile using the template
        user_profile = await client.read_resource("users://101/profile")
        print(f"User 101 profile: {user_profile}")

        # Get the 'summarize' prompt structure (doesn't execute the LLM call here)
        prompt_messages = await client.get_prompt("summarize", {"text": "This is some text."})
        print(f"Summarize prompt structure: {prompt_messages}")

if __name__ == "__main__":
    asyncio.run(test_server_locally())
    mcp.run(transport="sse", port=8080, host="0.0.0.0", log_level="DEBUG")
    # https://apidog.com/blog/fastmcp/
