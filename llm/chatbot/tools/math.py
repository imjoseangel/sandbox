from typing import List
from llama_index.core.tools import FunctionTool


class MathTool:
    """MathTool provides mathematical operations using FunctionTool."""

    @staticmethod
    def sum_numbers(a: float, b: float) -> float:
        """Add two numbers together.

        Args:
            a (float): The first number
            b (float): The second number

        Returns:
            float: The sum of a and b
        """
        return a + b

    @staticmethod
    def subtract_numbers(a: float, b: float) -> float:
        """Subtract the second number from the first number.

        Args:
            a (float): The first number (minuend)
            b (float): The second number (subtrahend)

        Returns:
            float: The result of a - b
        """
        return a - b

    @staticmethod
    def to_tool_list() -> List[FunctionTool]:
        """Convert math functions to FunctionTool list with descriptions and return_direct."""

        sum_tool = FunctionTool.from_defaults(
            fn=MathTool.sum_numbers,
            name="sum_numbers",
            description="""
                Use this tool to add two numbers together. Provide the two numbers as arguments.
            """,
            return_direct=True,
        )

        subtract_tool = FunctionTool.from_defaults(
            fn=MathTool.subtract_numbers,
            name="subtract_numbers",
            description="""
                Use this tool to subtract the second number from the first number.
                Provide the minuend and subtrahend as arguments.
            """,
            return_direct=True,
        )

        return [sum_tool, subtract_tool]
