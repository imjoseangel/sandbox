from llama_index.core.tools.tool_spec.base import BaseToolSpec


class MathTool(BaseToolSpec):
    """MathTool is a base class for mathematical operations.
    It provides methods to perform basic arithmetic operations like sum and subtract.
    """

    spec_functions = ["sum", "subtract"]

    def sum(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, minuend: float, subtrahend: float) -> float:
        return minuend - subtrahend
