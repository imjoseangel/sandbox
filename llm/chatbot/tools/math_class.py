from typing import List
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class MathTool(BaseToolSpec):
    """Math Tool for basic arithmetic operations."""

    spec_functions = ["sum_numbers", "subtract_numbers"]

    def sum_numbers(self, a: float, b: float) -> float:
        """Add two numbers together.

        Args:
            a (float): The first number
            b (float): The second number

        Returns:
            float: The sum of a and b
        """
        return a + b

    def subtract_numbers(self, a: float, b: float) -> float:
        """Subtract the second number from the first number.

        Args:
            a (float): The first number (minuend)
            b (float): The second number (subtrahend)

        Returns:
            float: The result of a - b
        """
        return a - b

    def to_tool_list(
        self,
        spec_functions=None,
        func_to_metadata_mapping=None,
    ) -> List[FunctionTool]:
        """Convert math functions to FunctionTool list with
        custom descriptions and return_direct."""

        # Create tools with custom descriptions and return_direct=True
        sum_tool = FunctionTool.from_defaults(
            fn=self.sum_numbers,
            name="sum_numbers",
            description="""
                Use this tool to add two numbers together.
                Provide the two numbers as arguments and get their sum.
            """,
            return_direct=True,
        )

        subtract_tool = FunctionTool.from_defaults(
            fn=self.subtract_numbers,
            name="subtract_numbers",
            description="""
                Use this tool to subtract the second number from the first number.
                Provide the minuend and subtrahend as arguments.
            """,
            return_direct=True,
        )

        return [sum_tool, subtract_tool]
