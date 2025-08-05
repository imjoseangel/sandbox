"""Agent configuration recommendations for direct tool usage."""

# Example agent configuration to reduce overthinking
AGENT_SYSTEM_PROMPT = """You are a helpful math assistant. When a user asks for mathematical calculations:

1. IMMEDIATELY use the appropriate tool without explanation
2. Do NOT show your reasoning or thought process
3. Do NOT explain the steps
4. ONLY use the tools provided for calculations

For addition: use sum_numbers
For subtraction: use subtract_numbers

Be direct and concise."""

# Alternative more forceful prompt
DIRECT_TOOL_PROMPT = """You are a calculator. Use tools immediately for any math question. No explanations, no thinking out loud, just use the tool and return the result."""

# Configuration for ReActAgent to reduce verbosity
REACT_AGENT_CONFIG = {
    "verbose": False,
    "max_iterations": 1,  # Force single tool use
    "return_direct": True,  # Should already be set on tools
}

# Example of how to configure the agent (pseudo-code)
"""
from llama_index.core.agent import ReActAgent

agent = ReActAgent.from_tools(
    tools=math_tool.to_tool_list(),
    system_prompt=DIRECT_TOOL_PROMPT,
    verbose=False,
    max_iterations=1
)
"""
