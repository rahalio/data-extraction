"""
Utilities Module

Helper functions and utilities for data manipulation.
"""

from .file_utils import (
    FileHandlingError,
    validate_directory,
    validate_file,
    safe_read_json,
    safe_write_json,
    get_matching_files,
    ensure_writable_output,
    get_file_size_mb,
    format_file_size,
)

from .logging_utils import (
    setup_logging,
    log_operation_summary,
)

from .progress_utils import (
    ProgressBar,
    progress_context,
    Spinner,
)

__all__ = [
    # File utilities
    "FileHandlingError",
    "validate_directory",
    "validate_file",
    "safe_read_json",
    "safe_write_json",
    "get_matching_files",
    "ensure_writable_output",
    "get_file_size_mb",
    "format_file_size",
    # Logging utilities
    "setup_logging",
    "log_operation_summary",
    # Progress utilities
    "ProgressBar",
    "progress_context",
    "Spinner",
]
