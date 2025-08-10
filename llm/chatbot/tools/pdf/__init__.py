import logging
from tools.pdf.base import DocumentTool

__version__ = "1.0.0"
__author__ = "Jose Angel Munoz"
__email__ = "josea.munoz@gmail.com"

# Export main classes and functions
__all__ = [
    "DocumentTool"
]

# Optional: Add convenience imports for commonly used types

# Set up library-level logging
logger = logging.getLogger(__name__)
# Prevent logging errors if no handler is configured
logger.addHandler(logging.NullHandler())
