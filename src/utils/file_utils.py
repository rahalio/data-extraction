"""
File handling utilities for data extraction tools

Provides safe file operations with validation and error handling.
"""
import os
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


class FileHandlingError(Exception):
    """Custom exception for file handling errors"""
    pass


def validate_directory(dir_path: Union[str, Path], create: bool = False) -> Path:
    """
    Validate that a directory exists and is accessible.

    Args:
        dir_path: Path to directory
        create: If True, create directory if it doesn't exist

    Returns:
        Path object representing the validated directory

    Raises:
        FileHandlingError: If directory is invalid or inaccessible
    """
    path = Path(dir_path).resolve()

    if not path.exists():
        if create:
            try:
                path.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {path}")
            except Exception as e:
                raise FileHandlingError(f"Failed to create directory '{path}': {e}")
        else:
            raise FileHandlingError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise FileHandlingError(f"Path is not a directory: {path}")

    if not os.access(path, os.R_OK):
        raise FileHandlingError(f"Directory is not readable: {path}")

    return path


def validate_file(file_path: Union[str, Path], must_exist: bool = True) -> Path:
    """
    Validate that a file exists and is accessible.

    Args:
        file_path: Path to file
        must_exist: If True, file must already exist

    Returns:
        Path object representing the validated file

    Raises:
        FileHandlingError: If file is invalid or inaccessible
    """
    path = Path(file_path).resolve()

    if must_exist:
        if not path.exists():
            raise FileHandlingError(f"File does not exist: {path}")

        if not path.is_file():
            raise FileHandlingError(f"Path is not a file: {path}")

        if not os.access(path, os.R_OK):
            raise FileHandlingError(f"File is not readable: {path}")
    else:
        # Validate parent directory exists and is writable
        parent = path.parent
        if not parent.exists():
            raise FileHandlingError(f"Parent directory does not exist: {parent}")

        if not os.access(parent, os.W_OK):
            raise FileHandlingError(f"Parent directory is not writable: {parent}")

    return path


def safe_read_json(file_path: Union[str, Path]) -> Any:
    """
    Safely read and parse a JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileHandlingError: If file cannot be read or parsed
    """
    path = validate_file(file_path, must_exist=True)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Successfully read JSON file: {path}")
        return data
    except json.JSONDecodeError as e:
        raise FileHandlingError(f"Invalid JSON in file '{path}': {e}")
    except Exception as e:
        raise FileHandlingError(f"Failed to read file '{path}': {e}")


def safe_write_json(
    data: Any,
    file_path: Union[str, Path],
    indent: int = 4,
    backup: bool = False
) -> Path:
    """
    Safely write data to a JSON file.

    Args:
        data: Data to write
        file_path: Path to output file
        indent: JSON indentation level
        backup: If True and file exists, create backup first

    Returns:
        Path to written file

    Raises:
        FileHandlingError: If file cannot be written
    """
    path = validate_file(file_path, must_exist=False)

    # Create backup if requested and file exists
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + '.bak')
        try:
            path.rename(backup_path)
            logger.info(f"Created backup: {backup_path}")
        except Exception as e:
            raise FileHandlingError(f"Failed to create backup: {e}")

    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        logger.info(f"Successfully wrote JSON file: {path}")
        return path
    except Exception as e:
        raise FileHandlingError(f"Failed to write file '{path}': {e}")


def get_matching_files(
    directory: Union[str, Path],
    pattern: str = "*.json",
    recursive: bool = False
) -> List[Path]:
    """
    Get list of files matching a pattern in a directory.

    Args:
        directory: Directory to search
        pattern: Glob pattern for matching files
        recursive: If True, search recursively

    Returns:
        List of matching file paths

    Raises:
        FileHandlingError: If directory is invalid
    """
    dir_path = validate_directory(directory)

    try:
        if recursive:
            files = list(dir_path.rglob(pattern))
        else:
            files = list(dir_path.glob(pattern))

        # Filter out directories, only return files
        files = [f for f in files if f.is_file()]

        logger.debug(f"Found {len(files)} files matching '{pattern}' in {dir_path}")
        return sorted(files)
    except Exception as e:
        raise FileHandlingError(f"Failed to search directory '{dir_path}': {e}")


def ensure_writable_output(file_path: Union[str, Path]) -> Path:
    """
    Ensure output file path is valid and writable.

    Args:
        file_path: Desired output file path

    Returns:
        Validated Path object

    Raises:
        FileHandlingError: If path is not writable
    """
    path = Path(file_path).resolve()

    # Check if file exists and is writable
    if path.exists():
        if not os.access(path, os.W_OK):
            raise FileHandlingError(f"Output file is not writable: {path}")
    else:
        # Check if parent directory is writable
        parent = path.parent
        if not parent.exists():
            try:
                parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise FileHandlingError(f"Cannot create output directory: {e}")

        if not os.access(parent, os.W_OK):
            raise FileHandlingError(f"Output directory is not writable: {parent}")

    return path


def get_file_size_mb(file_path: Union[str, Path]) -> float:
    """
    Get file size in megabytes.

    Args:
        file_path: Path to file

    Returns:
        File size in MB
    """
    path = Path(file_path)
    if path.exists():
        return path.stat().st_size / (1024 * 1024)
    return 0.0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
