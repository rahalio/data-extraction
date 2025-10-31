"""
JSON File Combiner

Combines multiple JSON files from a directory into a single JSON file.
Supports both list and object JSON formats with comprehensive error handling.
"""
import sys
from pathlib import Path
from typing import List, Union, Dict, Any, Optional
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import (
    FileHandlingError,
    validate_directory,
    safe_read_json,
    safe_write_json,
    get_matching_files,
    ensure_writable_output,
    setup_logging,
    log_operation_summary,
    ProgressBar,
    format_file_size,
)


logger = setup_logging("json_combiner")


class JSONCombinerError(Exception):
    """Custom exception for JSON combiner errors"""
    pass


def combine_json_files(
    input_dir: Union[str, Path] = ".",
    output_file: Union[str, Path] = "combined.json",
    pattern: str = "*.json",
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Combine multiple JSON files into a single JSON file.

    Args:
        input_dir: Directory containing JSON files (default: current directory)
        output_file: Name of the output combined JSON file
        pattern: Glob pattern for matching JSON files (default: *.json)
        verbose: Enable verbose logging

    Returns:
        Dictionary with statistics about the operation

    Raises:
        JSONCombinerError: If operation fails
    """
    start_time = time.time()

    if verbose:
        logger.setLevel(10)  # DEBUG

    logger.info(f"🚀 Starting JSON file combination...")
    logger.debug(f"Input directory: {input_dir}")
    logger.debug(f"Output file: {output_file}")
    logger.debug(f"Pattern: {pattern}")

    try:
        # Validate input directory
        input_path = validate_directory(input_dir)

        # Get matching files
        json_files = get_matching_files(input_path, pattern)

        if not json_files:
            raise JSONCombinerError(f"No files matching pattern '{pattern}' found in {input_path}")

        # Prepare output path
        if Path(output_file).is_absolute():
            output_path = Path(output_file)
        else:
            output_path = input_path / output_file

        output_path = ensure_writable_output(output_path)

        # Filter out the output file from processing
        json_files = [f for f in json_files if f != output_path]

        if not json_files:
            raise JSONCombinerError(f"No input files to process (output file excluded)")

        logger.info(f"📁 Found {len(json_files)} JSON files to combine")

        # Process files
        combined_data = []
        files_processed = 0
        files_skipped = 0
        errors = []

        progress = ProgressBar(len(json_files), prefix="Combining files")

        for json_file in json_files:
            try:
                data = safe_read_json(json_file)
                if isinstance(data, list):
                    combined_data.extend(data)
                else:
                    combined_data.append(data)
                files_processed += 1
        except json.JSONDecodeError as e:
            error_msg = f"Error reading {file_name}: {e}"
            errors.append(error_msg)
            print(f"⚠️ {error_msg}")
            files_skipped += 1
        except Exception as e:
            error_msg = f"Unexpected error with {file_name}: {e}"
            errors.append(error_msg)
            print(f"⚠️ {error_msg}")
            files_skipped += 1

    # Write the combined JSON file
    output_path = input_path / output_file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)

    result = {
        "files_processed": files_processed,
        "files_skipped": files_skipped,
        "total_records": len(combined_data),
        "output_file": str(output_path),
        "errors": errors
    }

    print(f"✅ Combined {files_processed} files into {output_file}")
    print(f"📊 Total records: {len(combined_data)}")
    if files_skipped > 0:
        print(f"⚠️ Skipped {files_skipped} files due to errors")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Combine multiple JSON files into a single JSON file"
    )
    parser.add_argument(
        "--input-dir",
        default=".",
        help="Directory containing JSON files (default: current directory)"
    )
    parser.add_argument(
        "--output",
        default="combined.json",
        help="Output filename (default: combined.json)"
    )
    parser.add_argument(
        "--pattern",
        default="*.json",
        help="Glob pattern for matching files (default: *.json)"
    )

    args = parser.parse_args()
    combine_json_files(args.input_dir, args.output, args.pattern)
