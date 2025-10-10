"""
Logging utilities for the API.
"""

import os
import logging
from ..config import LOG_FORMAT, LOG_DATE_FORMAT, LOG_LEVEL, get_log_dir


class ChromaDBTelemetryFilter(logging.Filter):
    """Filter to suppress ChromaDB telemetry-related error messages."""
    
    def filter(self, record):
        """Filter out telemetry-related error messages."""
        message = record.getMessage()
        # Suppress telemetry-related error messages
        if "Failed to send telemetry event" in message:
            return False
        if "capture() takes 1 positional argument but 3 were given" in message:
            return False
        return True


def setup_logging():
    """Set up logging to both console and file."""
    log_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Create logs directory if it doesn't exist
    log_dir = get_log_dir()
    os.makedirs(log_dir, exist_ok=True)
    
    # Get logger and clear any existing handlers to prevent duplicates
    logger = logging.getLogger("api")
    if logger.handlers:
        logger.handlers.clear()
    
    # Set up file handler
    log_file = os.path.join(log_dir, "api.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    
    # Configure logger
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger to avoid duplicate entries
    logger.propagate = False
    
    # Add ChromaDB telemetry filter to all handlers
    telemetry_filter = ChromaDBTelemetryFilter()
    for handler in logger.handlers:
        handler.addFilter(telemetry_filter)
    
    # Also apply to root logger to catch other ChromaDB messages
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(telemetry_filter)
    
    return logger


def get_logger():
    """Get the API logger instance."""
    return logging.getLogger("api")
