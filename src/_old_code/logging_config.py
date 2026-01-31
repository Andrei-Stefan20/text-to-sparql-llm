"""
Centralized logging configuration for the entire project.
Ensures consistent logging format and behavior across all modules.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Configures and returns a logger with consistent formatting.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to disk
        name: Logger name (if None, returns root logger)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    # Console handler with color support
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Detailed format with timestamp
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Gets or creates a logger with the standard configuration.

    Args:
        name: Logger name (typically __name__ from calling module)

    Returns:
        Configured logger instance
    """
    return setup_logging(name=name)
