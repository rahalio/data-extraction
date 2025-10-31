"""
LinkedIn Sales Navigator Data Extraction Workflow

This script provides a complete workflow for processing LinkedIn Sales Navigator exports:
1. Combine multiple JSON files into one
2. Convert the combined data to CSV format

Usage:
    python workflows/salesnav_workflow.py --input-dir /path/to/json/files --output-dir /path/to/output
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from combiners.json_combiner import combine_json_files
from converters.linkedin_json_to_csv import convert_json_to_csv


def salesnav_workflow(input_dir: str, output_dir: str = None, keep_combined: bool = False):
    """
    Complete workflow for processing LinkedIn Sales Navigator exports.

    Args:
        input_dir: Directory containing JSON export files
        output_dir: Directory for output files (default: same as input_dir)
        keep_combined: Keep the intermediate combined.json file (default: False)

    Returns:
        Dictionary with workflow results
    """
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve() if output_dir else input_path

    print("=" * 70)
    print("LinkedIn Sales Navigator Data Extraction Workflow")
    print("=" * 70)
    print(f"\n📂 Input directory: {input_path}")
    print(f"📁 Output directory: {output_path}\n")

    # Step 1: Combine JSON files
    print("Step 1: Combining JSON files...")
    print("-" * 70)

    combined_file = "combined_salesnav.json"
    combine_result = combine_json_files(
        input_dir=str(input_path),
        output_file=combined_file,
        pattern="*.json"
    )

    if combine_result["files_processed"] == 0:
        print("❌ No JSON files found to process!")
        return {"success": False, "error": "No JSON files found"}

    print(f"✅ Combined {combine_result['files_processed']} files")
    print(f"📊 Total records: {combine_result['total_records']}\n")

    # Step 2: Convert to CSV
    print("Step 2: Converting to CSV...")
    print("-" * 70)

    csv_file = "linkedin_companies.csv"
    convert_result = convert_json_to_csv(
        input_pattern=combined_file,
        output_file=str(output_path / csv_file),
        input_dir=str(input_path)
    )

    print(f"✅ CSV created with {convert_result['rows_written']} rows")
    print(f"📄 Output: {output_path / csv_file}\n")

    # Clean up combined file if requested
    if not keep_combined:
        combined_path = input_path / combined_file
        if combined_path.exists():
            combined_path.unlink()
            print(f"🗑️  Removed temporary file: {combined_file}\n")

    # Summary
    print("=" * 70)
    print("✅ Workflow Complete!")
    print("=" * 70)
    print(f"📊 Summary:")
    print(f"   • JSON files processed: {combine_result['files_processed']}")
    print(f"   • Total companies extracted: {convert_result['rows_written']}")
    print(f"   • Output CSV: {output_path / csv_file}")
    print("=" * 70 + "\n")

    return {
        "success": True,
        "files_processed": combine_result['files_processed'],
        "companies_extracted": convert_result['rows_written'],
        "output_csv": str(output_path / csv_file),
        "combine_result": combine_result,
        "convert_result": convert_result
    }


def main():
    parser = argparse.ArgumentParser(
        description="Process LinkedIn Sales Navigator JSON exports into a single CSV file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process JSON files in current directory
  python workflows/salesnav_workflow.py --input-dir ./data

  # Process files and save output elsewhere
  python workflows/salesnav_workflow.py --input-dir ./raw_data --output-dir ./processed

  # Keep the intermediate combined JSON file
  python workflows/salesnav_workflow.py --input-dir ./data --keep-combined
        """
    )

    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing LinkedIn Sales Navigator JSON export files"
    )

    parser.add_argument(
        "--output-dir",
        help="Directory for output files (default: same as input-dir)"
    )

    parser.add_argument(
        "--keep-combined",
        action="store_true",
        help="Keep the intermediate combined.json file"
    )

    args = parser.parse_args()

    try:
        result = salesnav_workflow(
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            keep_combined=args.keep_combined
        )

        if not result.get("success"):
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
