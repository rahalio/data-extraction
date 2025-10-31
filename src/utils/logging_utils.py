"""
Logging configuration for data extraction tools

Provides consistent logging setup across all modules.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for terminal output"""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    ICONS = {
        'DEBUG': '🔍',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🔥',
    }

    def format(self, record):
        # Add color and icon
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.ICONS.get(levelname, '')} {self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    name: str = "data_extraction",
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    verbose: bool = False
) -> logging.Logger:
    """
    Set up logging configuration.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional file path for logging
        verbose: If True, use DEBUG level

    Returns:
        Configured logger instance
    """
    if verbose:
        level = logging.DEBUG

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers.clear()

    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = ColoredFormatter(
        '%(levelname)s %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler if requested
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Always debug in file
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def log_operation_summary(
    logger: logging.Logger,
    operation: str,
    stats: dict,
    duration: Optional[float] = None
):
    """
    Log a formatted summary of an operation.

    Args:
        logger: Logger instance
        operation: Operation name
        stats: Dictionary of statistics to log
        duration: Optional duration in seconds
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"📊 {operation} - Summary")
    logger.info(f"{'='*60}")

    for key, value in stats.items():
        # Format key nicely
        formatted_key = key.replace('_', ' ').title()
        logger.info(f"  {formatted_key}: {value}")

    if duration:
        logger.info(f"  Duration: {duration:.2f}s")

    logger.info(f"{'='*60}\n")
