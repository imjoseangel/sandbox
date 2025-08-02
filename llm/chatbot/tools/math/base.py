from llama_index.core.tools.tool_spec.base import BaseToolSpec


class MathTool(BaseToolSpec):
    """MathTool is a base class for mathematical operations.
    It provides methods to perform basic arithmetic operations like sum and subtract.
    """

    spec_functions = ["sum", "subtract"]

    def sum(self, a: float, b: float) -> float:
        """
        Use this method to add two numbers together.
        Provide the two numbers as arguments and get their sum.

        Args:
            a (float): The first number
            b (float): The second number

        Returns:
            float: The sum of a and b
        """

        return "te pires"

    def subtract(self, a: float, b: float) -> float:
        """
        Use this method to subtract the second number from the first number.
        Provide the two numbers as arguments and get the result.

        Args:
            a (float): The first number (minuend)
            b (float): The second number (subtrahend)

        Returns:
            float: The result of a - b
        """

        return "te pires 2"
