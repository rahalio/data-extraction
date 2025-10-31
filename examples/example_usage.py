"""
Example Usage of Data Extraction Tools

This script demonstrates comprehensive usage of the data extraction library:
- Combining JSON files
- Converting LinkedIn data to CSV
- Using utility functions for file handling, logging, and progress tracking
"""

from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import main functions
from combiners import combine_json_files
from converters import convert_json_to_csv_enhanced

# Import utilities
from utils import (
    setup_logging,
    log_operation_summary,
    validate_directory,
    safe_read_json,
    ProgressBar,
    progress_context,
)


def example_1_combine_json():
    """Example 1: Combine multiple JSON files with progress tracking"""
    print("=" * 70)
    print("Example 1: Combining JSON Files")
    print("=" * 70)

    logger = setup_logging("example1", verbose=True)

    # Combine all JSON files in a directory
    try:
        result = combine_json_files(
            input_dir="./sample_data",
            output_file="combined_output.json",
            pattern="*.json"
        )

        log_operation_summary(
            logger,
            operation="JSON Combine",
            success=True,
            **result
        )
    except Exception as e:
        logger.error(f"Failed to combine files: {e}")

    print()


def example_2_linkedin_to_csv():
    """Example 2: Convert LinkedIn JSON to CSV with enhanced features"""
    print("=" * 70)
    print("Example 2: Converting LinkedIn JSON to CSV")
    print("=" * 70)

    logger = setup_logging("example2", verbose=True)

    # Convert LinkedIn Sales Navigator data
    try:
        result = convert_json_to_csv_enhanced(
            input_pattern="*.json",
            output_file="linkedin_companies.csv",
            input_dir="./sample_data"
        )

        log_operation_summary(
            logger,
            operation="LinkedIn CSV Export",
            success=True,
            **result
        )
    except Exception as e:
        logger.error(f"Failed to convert files: {e}")

    print()


def example_3_utility_functions():
    """Example 3: Using utility functions directly"""
    print("=" * 70)
    print("Example 3: Using Utility Functions")
    print("=" * 70)

    logger = setup_logging("example3", verbose=True)

    # Validate directory
    try:
        data_dir = validate_directory("./sample_data")
        logger.info(f"✓ Validated directory: {data_dir}")
    except Exception as e:
        logger.warning(f"Directory validation failed: {e}")

    # Read JSON safely
    try:
        data = safe_read_json("./sample_data/test.json")
        logger.info(f"✓ Successfully read JSON file with {len(data)} items")
    except Exception as e:
        logger.warning(f"Could not read JSON: {e}")

    # Progress bar example
    print("\nProgress bar example:")
    with progress_context(total=100, desc="Processing") as progress:
        import time
        for i in range(100):
            time.sleep(0.01)  # Simulate work
            progress.update(1)

    print()


def example_4_complete_workflow():
    """Example 4: Complete workflow using all features"""
    print("=" * 70)
    print("Example 4: Complete Data Extraction Workflow")
    print("=" * 70)

    logger = setup_logging("workflow", verbose=True)

    input_dir = "./sample_data"
    output_dir = "./output"

    logger.info(f"Starting workflow: {input_dir} -> {output_dir}")

    try:
        # Step 1: Validate input directory
        validated_dir = validate_directory(input_dir)
        logger.info(f"✓ Input directory validated: {validated_dir}")

        # Step 2: Combine JSON files
        logger.info("Step 1/2: Combining JSON files...")
        combine_result = combine_json_files(
            input_dir=input_dir,
            output_file="combined.json",
            pattern="*.json"
        )
        logger.info(f"✓ Combined {combine_result['files_processed']} files")

        # Step 3: Convert to CSV
        logger.info("Step 2/2: Converting to CSV...")
        convert_result = convert_json_to_csv_enhanced(
            input_pattern="combined.json",
            output_file=f"{output_dir}/companies.csv",
            input_dir=input_dir
        )
        logger.info(f"✓ Created CSV with {convert_result['rows_written']} rows")

        # Summary
        log_operation_summary(
            logger,
            operation="Complete Workflow",
            success=True,
            files_processed=combine_result['files_processed'],
            rows_written=convert_result['rows_written'],
        )

    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        log_operation_summary(
            logger,
            operation="Complete Workflow",
            success=False,
            error=str(e)
        )

    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("Data Extraction Tools - Comprehensive Examples")
    print("=" * 70 + "\n")

    print("Available examples:")
    print("  1. Combine JSON files")
    print("  2. Convert LinkedIn JSON to CSV")
    print("  3. Use utility functions directly")
    print("  4. Complete workflow")
    print()

    # Uncomment to run examples (requires sample data)
    # example_1_combine_json()
    # example_2_linkedin_to_csv()
    # example_3_utility_functions()
    # example_4_complete_workflow()

    print("To run these examples:")
    print("1. Create a 'sample_data' directory")
    print("2. Add some JSON files to it")
    print("3. Uncomment the example function calls in main()")
    print("4. Run: python3 examples/usage_examples.py")
    print()


if __name__ == "__main__":
    main()