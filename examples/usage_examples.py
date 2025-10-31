"""
Example Usage of Data Extraction Tools

This script demonstrates how to use the data extraction tools
for combining JSON files and converting LinkedIn data to CSV.
"""

from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from combiners import combine_json_files
from converters import convert_json_to_csv


def example_combine_json():
    """Example: Combine multiple JSON files"""
    print("=" * 60)
    print("Example 1: Combining JSON Files")
    print("=" * 60)

    # Combine all JSON files in a directory
    result = combine_json_files(
        input_dir="./sample_data",
        output_file="combined_output.json",
        pattern="*.json"
    )

    print(f"\nResults:")
    print(f"  Files processed: {result['files_processed']}")
    print(f"  Total records: {result['total_records']}")
    print(f"  Output file: {result['output_file']}")
    print()


def example_linkedin_to_csv():
    """Example: Convert LinkedIn JSON to CSV"""
    print("=" * 60)
    print("Example 2: Converting LinkedIn JSON to CSV")
    print("=" * 60)

    # Convert LinkedIn Sales Navigator data
    result = convert_json_to_csv(
        input_pattern="*.json",
        output_file="linkedin_companies.csv",
        input_dir="./sample_data"
    )

    print(f"\nResults:")
    print(f"  Files processed: {result['files_processed']}")
    print(f"  Rows written: {result['rows_written']}")
    print(f"  Output file: {result['output_file']}")
    print()


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("Data Extraction Tools - Example Usage")
    print("=" * 60 + "\n")

    # You can uncomment these to run the examples
    # Make sure you have sample data in ./sample_data directory

    # example_combine_json()
    # example_linkedin_to_csv()

    print("To run these examples:")
    print("1. Create a 'sample_data' directory")
    print("2. Add some JSON files to it")
    print("3. Uncomment the function calls in main()")
    print()


if __name__ == "__main__":
    main()
