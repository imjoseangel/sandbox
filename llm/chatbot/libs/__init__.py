import logging

from libs.prompts import (ReactPrompt, SubQuestionPrompt,
                          QAPrompt, SynthesisPrompt, SystemPrompt)

__version__ = "1.0.0"
__author__ = "Jose Angel Munoz"
__email__ = "josea.munoz@gmail.com"

# Export main classes and functions
__all__ = [
    "SystemPrompt",
    "ReactPrompt",
    "SubQuestionPrompt",
    "QAPrompt",
    "SynthesisPrompt",
]

# Optional: Add convenience imports for commonly used types

# Set up library-level logging
logger = logging.getLogger(__name__)
# Prevent logging errors if no handler is configured
logger.addHandler(logging.NullHandler())

# Optional: Configuration constants
DEFAULT_SIMILARITY_TOP_K = 15
DEFAULT_ALPHA = 0.3
DEFAULT_MAX_KEYWORDS = 15
