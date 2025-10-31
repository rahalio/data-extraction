"""
Data Extraction Utilities

A comprehensive library for data manipulation, conversion, and combination.
Includes utilities for file handling, logging, and progress tracking.
"""

__version__ = "0.2.0"
__author__ = "rahalio"

# Combiners
from .combiners.json_combiner import combine_json_files

# Converters
from .converters.linkedin_json_to_csv import convert_json_to_csv
from .converters.linkedin_json_to_csv_enhanced import convert_linkedin_json_to_csv_enhanced

# Utilities
from .utils.file_utils import (
    validate_file_path,
    validate_directory_path,
    get_file_size_mb,
    safe_read_json,
    safe_write_json,
    safe_write_csv
)
from .utils.logging_utils import setup_logging, log_operation_summary
from .utils.progress_utils import ProgressTracker

__all__ = [
    # Combiners
    "combine_json_files",

    # Converters
    "convert_json_to_csv",
    "convert_linkedin_json_to_csv_enhanced",

    # File Utilities
    "validate_file_path",
    "validate_directory_path",
    "get_file_size_mb",
    "safe_read_json",
    "safe_write_json",
    "safe_write_csv",

    # Logging Utilities
    "setup_logging",
    "log_operation_summary",

    # Progress Utilities
    "ProgressTracker",
]
