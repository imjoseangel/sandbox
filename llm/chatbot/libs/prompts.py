def SystemPrompt() -> str:
    """Returns a direct system prompt for immediate action."""
    _SYSTEM_PROMPT = """
        You are a helpful assistant. For mathematical calculations, use the appropriate tools immediately without explanation.

        - For addition: use sum_numbers tool
        - For subtraction: use subtract_numbers tool
        - For other questions: answer directly from your knowledge

        Be concise and direct in your responses.
        """

    return _SYSTEM_PROMPT


def ReactPrompt() -> str:
    """Returns a ReActAgent prompt optimized for direct tool usage."""

    _REACT_AGENT_PROMPT = """You are designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

        ## Tools

        You have access to a wide variety of tools. You are responsible for using the tools in any sequence you deem appropriate to complete the task at hand.
        This may require breaking the task into subtasks and using different tools to complete each subtask.

        You have access to the following tools:
        {tool_desc}

        ## Tool Usage Guidelines

        **MATH OPERATIONS - USE TOOLS IMMEDIATELY:**
        - For addition (plus, +, add, sum): Use sum_numbers tool
        - For subtraction (minus, -, subtract, difference): Use subtract_numbers tool
        - Keep your Thought brief and go directly to Action

        **NON-MATH QUESTIONS:**
        - Answer directly from your knowledge without using tools

        ## Output Format

        Please answer in the same language as the question and use the following format:

        ```
        Thought: The current language of the user is: (user's language). I need to use a tool to help me answer the question.
        Action: tool name (one of {tool_names}) if using a tool.
        Action Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})
        ```

        Please ALWAYS start with a Thought.

        NEVER surround your response with markdown code markers. You may use code markers within your response if you need to.

        Please use a valid JSON format for the Action Input. Do NOT do this {{'input': 'hello world', 'num_beams': 5}}.

        If this format is used, the tool will respond in the following format:

        ```
        Observation: tool response
        ```

        You should keep repeating the above format till you have enough information to answer the question without using any more tools. At that point, you MUST respond in one of the following two formats:

        ```
        Thought: I can answer without using any more tools. I'll use the user's language to answer
        Answer: [your answer here (In the same language as the user's question)]
        ```

        ```
        Thought: I cannot answer the question with the provided tools.
        Answer: [your answer here (In the same language as the user's question)]
        ```

        ## Current Conversation

        Below is the current conversation consisting of interleaving human and assistant messages.
        """

    return _REACT_AGENT_PROMPT


def SubQuestionPrompt() -> str:
    _SUB_QUESTION_PROMPT = """
        Given a user question, and a list of tools, output a list of relevant sub-questions \
        in json markdown that when composed can help answer the full user question:

        # Example 1
        <Tools>
        ```json
        {{
            "sum_numbers": "Add two numbers together",
            "subtract_numbers": "Subtract one number from another"
        }}
        ```

        <User Question>
        What is 15 plus 8 minus 3?

        <Output>
        ```json
        {{
            "items": [
                {{
                    "sub_question": "What is 15 plus 8?",
                    "tool_name": "sum_numbers"
                }},
                {{
                    "sub_question": "What is the result minus 3?",
                    "tool_name": "subtract_numbers"
                }}
            ]
        }}
        ```

        # Example 2
        <Tools>
        ```json
        {tools_str}
        ```

        <User Question>
        {query_str}

        <Output>
        """

    return _SUB_QUESTION_PROMPT


def QAPrompt() -> str:
    _CUSTOM_QA_PROMPT = """
         You are an assistant helping to answer questions, with access to math tools for calculations.
         For mathematical operations (addition and subtraction), use the appropriate tools.
         For other questions, provide answers based on your general knowledge.
         ---------------------
         {context_str}
         ---------------------
         Given the context information and not prior knowledge, answer the query concisely.
         Query: {query_str}
         Answer:
         """
    return _CUSTOM_QA_PROMPT


def SynthesisPrompt() -> str:
    _SYNTHESIS_PROMPT = """
            The following are answers to sub-questions, derived from an original query.
            Each sub-answer may contain mathematical results or general information.
            ---------------------
            {context_str}
            ---------------------
            Given these sub-answers, synthesize a comprehensive final answer to the original query: {query_str}
            Ensure all mathematical calculations are accurate and clearly presented.
            Final Answer:
            """
    return _SYNTHESIS_PROMPT
