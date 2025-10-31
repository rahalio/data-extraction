#!/usr/bin/env python3
"""
Enhanced LinkedIn JSON to CSV Converter

Converts LinkedIn Sales Navigator company data from JSON format to CSV,
with comprehensive error handling, validation, and progress tracking.

Features:
- Robust error handling and validation
- Progress tracking for large datasets
- Detailed logging and statistics
- Data deduplication
- Flexible field mapping
"""

import os
import sys
import json
import csv
import argparse
import logging
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.file_utils import (
    validate_directory,
    get_matching_files,
    safe_read_json,
    ensure_writable_output
)
from utils.logging_utils import setup_logging, log_operation_summary
from utils.progress_utils import ProgressBar

# Configure logger
logger = logging.getLogger(__name__)


class LinkedInDataExtractor:
    """Extracts and transforms LinkedIn Sales Navigator data"""

    # CSV field definitions
    CSV_FIELDS = [
        "companyName",
        "industry",
        "employeeCountRange",
        "employeeDisplayCount",
        "listCount",
        "saved",
        "entityUrn",
        "linkedin_url",
        "recipeType",
        "trackingId",
        "description",
        "logo_100",
        "logo_200",
        "logo_400",
        "spotlightBadges",
        "source_file",
    ]

    def __init__(self, verbose: bool = False):
        """
        Initialize the LinkedIn data extractor.

        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.stats = defaultdict(int)
        self.seen_urns: Set[str] = set()

    def pick_artifact_url(self, pic: Optional[Dict], target_width: int) -> str:
        """
        Extract the artifact URL for a given width from a picture object.

        Args:
            pic: Picture object containing rootUrl and artifacts
            target_width: Desired width for the artifact

        Returns:
            Full URL to the artifact, or empty string if not found
        """
        try:
            if not pic:
                return ""

            root = pic.get("rootUrl", "")
            artifacts = pic.get("artifacts") or []

            # Find artifact with target width
            chosen = next((a for a in artifacts if a.get("width") == target_width), None)

            # Fallback to first artifact if target not found
            if not chosen and artifacts:
                chosen = artifacts[0]

            if root and chosen and chosen.get("fileIdentifyingUrlPathSegment"):
                return root + chosen["fileIdentifyingUrlPathSegment"]

            return ""
        except Exception as e:
            logger.debug(f"Error extracting artifact URL: {e}")
            return ""

    def join_badges(self, badges: Optional[List[Dict]]) -> str:
        """
        Join badge information into a single string.

        Args:
            badges: List of badge dictionaries

        Returns:
            Pipe-separated string of badge information
        """
        try:
            if not badges:
                return ""

            parts = []
            for b in badges:
                label = b.get("id", "")
                display = b.get("displayValue", "")
                if label or display:
                    parts.append(f"{label}: {display}".strip(": "))

            return " | ".join(parts)
        except Exception as e:
            logger.debug(f"Error joining badges: {e}")
            return ""

    def normalize_text(self, val: Any) -> str:
        """
        Normalize text by removing newlines and extra whitespace.

        Args:
            val: Value to normalize (will be converted to string)

        Returns:
            Normalized string
        """
        try:
            if val is None:
                return ""
            s = str(val)
            return " ".join(s.replace("\r", " ").replace("\n", " ").split()).strip()
        except Exception as e:
            logger.debug(f"Error normalizing text: {e}")
            return ""

    def build_linkedin_url(self, entity_urn: str) -> str:
        """
        Extract company code from entityUrn and build the LinkedIn Sales URL.

        Args:
            entity_urn: LinkedIn entity URN (e.g., "urn:li:company:12345")

        Returns:
            Full LinkedIn Sales Navigator company URL
        """
        try:
            if not entity_urn or ":" not in entity_urn:
                return ""
            company_code = entity_urn.split(":")[-1]
            return f"https://www.linkedin.com/sales/company/{company_code}"
        except Exception as e:
            logger.debug(f"Error building LinkedIn URL: {e}")
            return ""

    def extract_row(self, rec: Dict[str, Any], source_file: str) -> Optional[Dict[str, Any]]:
        """
        Build a flattened row from a JSON record.

        Args:
            rec: JSON record dictionary
            source_file: Name of the source file

        Returns:
            Flattened dictionary suitable for CSV output, or None if invalid
        """
        try:
            # Validate required fields
            if not isinstance(rec, dict):
                self.stats['invalid_records'] += 1
                return None

            entity_urn = rec.get("entityUrn", "")

            # Check for duplicates
            if entity_urn and entity_urn in self.seen_urns:
                self.stats['duplicate_records'] += 1
                if self.verbose:
                    logger.debug(f"Duplicate entity URN found: {entity_urn}")
                return None

            if entity_urn:
                self.seen_urns.add(entity_urn)

            # Extract picture and badges
            pic = rec.get("companyPictureDisplayImage") or {}
            badges = rec.get("spotlightBadges") or []

            # Build row
            row = {
                "companyName": rec.get("companyName", ""),
                "industry": rec.get("industry", ""),
                "employeeCountRange": rec.get("employeeCountRange", ""),
                "employeeDisplayCount": rec.get("employeeDisplayCount", ""),
                "listCount": rec.get("listCount", ""),
                "saved": rec.get("saved", ""),
                "entityUrn": entity_urn,
                "linkedin_url": self.build_linkedin_url(entity_urn),
                "recipeType": rec.get("$recipeType", ""),
                "trackingId": rec.get("trackingId", ""),
                "description": self.normalize_text(rec.get("description", "")),
                "logo_100": self.pick_artifact_url(pic, 100),
                "logo_200": self.pick_artifact_url(pic, 200),
                "logo_400": self.pick_artifact_url(pic, 400),
                "spotlightBadges": self.join_badges(badges),
                "source_file": os.path.basename(source_file),
            }

            self.stats['valid_records'] += 1
            return row

        except Exception as e:
            logger.warning(f"Error extracting row from {source_file}: {e}")
            self.stats['extraction_errors'] += 1
            return None

    def process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a single JSON file and extract rows.

        Args:
            file_path: Path to the JSON file

        Returns:
            List of extracted row dictionaries
        """
        rows = []

        try:
            # Read JSON file
            data = safe_read_json(file_path)
            if data is None:
                self.stats['failed_files'] += 1
                return rows

            # Normalize to list
            if isinstance(data, list):
                records = data
            else:
                records = [data]

            # Extract rows
            for rec in records:
                if isinstance(rec, dict):
                    row = self.extract_row(rec, file_path)
                    if row:
                        rows.append(row)

            self.stats['processed_files'] += 1

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            self.stats['failed_files'] += 1

        return rows


def convert_json_to_csv(
    input_pattern: str = "*.json",
    output_file: str = "companies.csv",
    input_dir: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Convert LinkedIn JSON files to CSV format.

    Args:
        input_pattern: Glob pattern for input JSON files
        output_file: Output CSV filename
        input_dir: Directory containing JSON files (default: current directory)
        verbose: Enable verbose logging

    Returns:
        Dictionary with statistics about the conversion
    """
    # Setup logging
    setup_logging(verbose=verbose)

    logger.info("Starting LinkedIn JSON to CSV conversion")
    logger.info(f"Pattern: {input_pattern}")
    logger.info(f"Output: {output_file}")

    # Validate input directory
    if input_dir:
        try:
            validated_dir = validate_directory(input_dir)
            os.chdir(validated_dir)
        except Exception as e:
            logger.error(f"Invalid input directory: {e}")
            return {"success": False, "error": str(e)}

    # Get input files
    try:
        files = get_matching_files(
            directory=".",
            pattern=input_pattern,
            recursive=False
        )
        # Exclude output file
        files = [f for f in files if f.name != output_file]
    except Exception as e:
        logger.error(f"Error finding files: {e}")
        return {"success": False, "error": str(e)}

    if not files:
        logger.warning(f"No files found matching pattern: {input_pattern}")
        return {"success": False, "error": "No matching files found"}

    logger.info(f"Found {len(files)} files to process")

    # Initialize extractor
    extractor = LinkedInDataExtractor(verbose=verbose)
    all_rows = []

    # Process files with progress bar
    progress = ProgressBar(len(files), prefix="Processing files")

    for i, file_path in enumerate(files):
        if verbose:
            logger.info(f"Processing: {file_path}")

        rows = extractor.process_file(file_path)
        all_rows.extend(rows)

        progress.update(i + 1)

    progress.finish()

    # Write CSV file
    try:
        logger.info(f"Writing {len(all_rows)} rows to {output_file}")

        with open(output_file, "w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=LinkedInDataExtractor.CSV_FIELDS)
            writer.writeheader()
            writer.writerows(all_rows)

        logger.info(f"✅ Successfully wrote {len(all_rows)} rows to {output_file}")

    except Exception as e:
        logger.error(f"Error writing CSV file: {e}")
        return {
            "success": False,
            "error": f"Failed to write CSV: {e}",
            "stats": extractor.stats
        }

    # Prepare result
    result = {
        "success": True,
        "files_processed": extractor.stats['processed_files'],
        "files_failed": extractor.stats['failed_files'],
        "rows_written": len(all_rows),
        "valid_records": extractor.stats['valid_records'],
        "invalid_records": extractor.stats['invalid_records'],
        "duplicate_records": extractor.stats['duplicate_records'],
        "extraction_errors": extractor.stats['extraction_errors'],
        "output_file": output_file
    }

    # Log summary
    log_operation_summary(
        logger=logger,
        operation="LinkedIn JSON to CSV Conversion",
        stats=result,
        duration=0  # TODO: Add timing
    )

    return result


def main():
    """Main entry point for CLI usage"""
    parser = argparse.ArgumentParser(
        description="Convert LinkedIn Sales Navigator JSON files to CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert all JSON files in current directory
  python linkedin_json_to_csv.py

  # Convert files from specific directory
  python linkedin_json_to_csv.py --input-dir ./data --output companies.csv

  # Use custom pattern with verbose output
  python linkedin_json_to_csv.py --pattern "export_*.json" --verbose
        """
    )

    parser.add_argument(
        "--pattern",
        default="*.json",
        help="Glob pattern for input JSON files (default: *.json)"
    )
    parser.add_argument(
        "--output",
        default="companies.csv",
        help="Output CSV filename (default: companies.csv)"
    )
    parser.add_argument(
        "--input-dir",
        help="Directory containing JSON files (default: current directory)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # Run conversion
    result = convert_json_to_csv(
        input_pattern=args.pattern,
        output_file=args.output,
        input_dir=args.input_dir,
        verbose=args.verbose
    )

    # Exit with appropriate code
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
