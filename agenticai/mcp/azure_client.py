from fastmcp import Client
import asyncio


async def main():
    # The client will automatically handle Azure OAuth
    async with Client("http://localhost:8000/mcp/", auth="oauth") as client:
        # First-time connection will open Azure login in your browser
        print("✓ Authenticated with Azure!")

        result = await client.call_tool("get_user_info")
        user_data = result.content[0].text  # Extract the actual data
        import json
        user_info = json.loads(user_data)  # Parse JSON string

        print(f"Azure user: {user_info['email']}")
        print(f"Name: {user_info['name']}")

if __name__ == "__main__":
    asyncio.run(main())
