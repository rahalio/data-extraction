"""
JSON File Combiner

Combines multiple JSON files from a directory into a single JSON file.
Supports both list and object JSON formats.
"""
import json
import glob
import os
from pathlib import Path
from typing import List, Union, Dict, Any


def combine_json_files(
    input_dir: str = ".",
    output_file: str = "combined.json",
    pattern: str = "*.json"
) -> Dict[str, Any]:
    """
    Combine multiple JSON files into a single JSON file.

    Args:
        input_dir: Directory containing JSON files (default: current directory)
        output_file: Name of the output combined JSON file
        pattern: Glob pattern for matching JSON files (default: *.json)

    Returns:
        Dictionary with statistics about the operation
    """
    # Resolve the input directory
    input_path = Path(input_dir).resolve()
    os.chdir(input_path)

    combined_data = []
    files_processed = 0
    files_skipped = 0
    errors = []

    # Find all JSON files matching the pattern
    json_files = glob.glob(pattern)

    for file_name in json_files:
        if file_name == output_file:
            continue  # skip the output file itself

        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
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
