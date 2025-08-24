from typing import List
from llama_index.core.tools import FunctionTool
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class MathTool(BaseToolSpec):
    """Math Tool for basic arithmetic operations."""

    spec_functions = ["sum_numbers", "subtract_numbers"]

    def sum_numbers(self, a: float, b: float) -> float:
        """Add two numbers together.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        return a + b

    def subtract_numbers(self, a: float, b: float) -> float:
        """Subtract the second number from the first number.

        Args:
            a: First number (minuend)
            b: Second number (subtrahend)

        Returns:
            Result of a - b
        """
        return a - b

    def to_tool_list(
        self,
        spec_functions=None,
        func_to_metadata_mapping=None,
    ) -> List[FunctionTool]:
        """Convert math functions to FunctionTool list with
        custom descriptions and return_direct."""

        # Create tools with concise descriptions and return_direct=True
        sum_tool = FunctionTool.from_defaults(
            fn=self.sum_numbers,
            name="sum_numbers",
            description="Calculate the sum of two numbers. Use for addition (+, plus, add, sum).",
            return_direct=True,
        )

        subtract_tool = FunctionTool.from_defaults(
            fn=self.subtract_numbers,
            name="subtract_numbers",
            description="Calculate the difference between two numbers. Use for subtraction (-, minus, subtract).",
            return_direct=True,
        )

        return [sum_tool, subtract_tool]
