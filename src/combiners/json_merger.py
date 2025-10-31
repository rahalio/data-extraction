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
        total_size = 0

        progress = ProgressBar(len(json_files), prefix="Combining files")

        for json_file in json_files:
            try:
                data = safe_read_json(json_file)

                # Track file size
                total_size += json_file.stat().st_size

                # Add data to combined list
                if isinstance(data, list):
                    combined_data.extend(data)
                    logger.debug(f"Added {len(data)} records from {json_file.name}")
                else:
                    combined_data.append(data)
                    logger.debug(f"Added 1 record from {json_file.name}")

                files_processed += 1

            except FileHandlingError as e:
                error_msg = f"Error reading {json_file.name}: {e}"
                errors.append(error_msg)
                logger.warning(error_msg)
                files_skipped += 1
            except Exception as e:
                error_msg = f"Unexpected error with {json_file.name}: {e}"
                errors.append(error_msg)
                logger.error(error_msg)
                files_skipped += 1
            finally:
                progress.update()

        progress.finish()

        if files_processed == 0:
            raise JSONCombinerError("No files were successfully processed")

        # Write combined output
        logger.info(f"💾 Writing combined data to {output_path.name}...")
        safe_write_json(combined_data, output_path, indent=4, backup=False)

        # Calculate statistics
        duration = time.time() - start_time
        output_size = output_path.stat().st_size

        result = {
            "files_processed": files_processed,
            "files_skipped": files_skipped,
            "total_records": len(combined_data),
            "input_size": format_file_size(total_size),
            "output_size": format_file_size(output_size),
            "output_file": str(output_path),
            "duration": f"{duration:.2f}s",
            "errors": errors
        }

        # Log summary
        log_operation_summary(logger, "JSON Combination", result, duration)

        return result

    except FileHandlingError as e:
        logger.error(f"File handling error: {e}")
        raise JSONCombinerError(f"File handling error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise JSONCombinerError(f"Unexpected error: {e}")


def main():
    """Main entry point for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Combine multiple JSON files into a single JSON file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Combine all JSON files in current directory
  python json_combiner.py

  # Combine files from specific directory
  python json_combiner.py --input-dir ./data --output combined.json

  # Use custom pattern
  python json_combiner.py --pattern "export_*.json" --verbose
        """
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
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    try:
        result = combine_json_files(
            args.input_dir,
            args.output,
            args.pattern,
            args.verbose
        )
        sys.exit(0)
    except JSONCombinerError as e:
        logger.error(f"❌ Failed to combine files: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Operation cancelled by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
