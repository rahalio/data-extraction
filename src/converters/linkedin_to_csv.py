"""
JSON to CSV Converter for LinkedIn Sales Navigator Data

Converts LinkedIn Sales Navigator company data from JSON format to CSV,
with data transformation, normalization, and URL building.
"""
import os
import glob
import json
import csv
import argparse
from typing import Dict, List, Any, Optional
from pathlib import Path


def pick_artifact_url(pic: Optional[Dict], target_width: int) -> str:
    """
    Extract the artifact URL for a given width from a picture object.

    Args:
        pic: Picture object containing rootUrl and artifacts
        target_width: Desired width for the artifact

    Returns:
        Full URL to the artifact, or empty string if not found
    """
    if not pic:
        return ""
    root = pic.get("rootUrl")
    artifacts = pic.get("artifacts") or []
    chosen = next((a for a in artifacts if a.get("width") == target_width), None)
    if not chosen and artifacts:
        chosen = artifacts[0]
    if root and chosen and chosen.get("fileIdentifyingUrlPathSegment"):
        return root + chosen["fileIdentifyingUrlPathSegment"]
    return ""


def join_badges(badges: Optional[List[Dict]]) -> str:
    """
    Join badge information into a single string.

    Args:
        badges: List of badge dictionaries

    Returns:
        Pipe-separated string of badge information
    """
    if not badges:
        return ""
    parts = []
    for b in badges:
        label = b.get("id") or ""
        display = b.get("displayValue") or ""
        if label or display:
            parts.append(f"{label}: {display}".strip(": "))
    return " | ".join(parts)


def normalize_text(val: Any) -> str:
    """
    Normalize text by removing newlines and extra whitespace.

    Args:
        val: Value to normalize (will be converted to string)

    Returns:
        Normalized string
    """
    if val is None:
        return ""
    s = str(val)
    return " ".join(s.replace("\r", " ").replace("\n", " ").split()).strip()


def build_linkedin_url(entity_urn: str) -> str:
    """
    Extract company code from entityUrn and build the LinkedIn Sales URL.

    Args:
        entity_urn: LinkedIn entity URN (e.g., "urn:li:company:12345")

    Returns:
        Full LinkedIn Sales Navigator company URL
    """
    if not entity_urn or ":" not in entity_urn:
        return ""
    company_code = entity_urn.split(":")[-1]
    return f"https://www.linkedin.com/sales/company/{company_code}"


def build_row(rec: Dict[str, Any], source_file: str) -> Dict[str, Any]:
    """
    Build a flattened row from a JSON record.

    Args:
        rec: JSON record dictionary
        source_file: Name of the source file

    Returns:
        Flattened dictionary suitable for CSV output
    """
    pic = rec.get("companyPictureDisplayImage") or {}
    badges = rec.get("spotlightBadges") or []
    entity_urn = rec.get("entityUrn", "")

    row = {
        "companyName": rec.get("companyName", ""),
        "industry": rec.get("industry", ""),
        "employeeCountRange": rec.get("employeeCountRange", ""),
        "employeeDisplayCount": rec.get("employeeDisplayCount", ""),
        "listCount": rec.get("listCount", ""),
        "saved": rec.get("saved", ""),
        "entityUrn": entity_urn,
        "linkedin_url": build_linkedin_url(entity_urn),
        "recipeType": rec.get("$recipeType", ""),
        "trackingId": rec.get("trackingId", ""),
        "description": normalize_text(rec.get("description", "")),
        "logo_100": pick_artifact_url(pic, 100),
        "logo_200": pick_artifact_url(pic, 200),
        "logo_400": pick_artifact_url(pic, 400),
        "spotlightBadges": join_badges(badges),
        "source_file": os.path.basename(source_file),
    }
    return row


def convert_json_to_csv(
    input_pattern: str = "*.json",
    output_file: str = "companies.csv",
    input_dir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert JSON files to CSV format.

    Args:
        input_pattern: Glob pattern for input JSON files
        output_file: Output CSV filename
        input_dir: Directory containing JSON files (default: current directory)

    Returns:
        Dictionary with statistics about the conversion
    """
    if input_dir:
        os.chdir(input_dir)

    files = sorted(glob.glob(input_pattern))
    if not files:
        print(f"⚠️ No files match pattern: {input_pattern}")
        return {"files_processed": 0, "rows_written": 0}

    fieldnames = [
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

    rows = []
    files_processed = 0
    files_skipped = 0

    for path in files:
        if os.path.basename(path) == output_file:
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            files_processed += 1
        except Exception as e:
            print(f"⚠️ Skipping {path}: {e}")
            files_skipped += 1
            continue

        if isinstance(data, list):
            records = data
        else:
            records = [data]

        for rec in records:
            if isinstance(rec, dict):
                rows.append(build_row(rec, path))

    with open(output_file, "w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Wrote {len(rows)} rows into {output_file}")
    print(f"📊 Processed {files_processed} files")
    if files_skipped > 0:
        print(f"⚠️ Skipped {files_skipped} files due to errors")

    return {
        "files_processed": files_processed,
        "files_skipped": files_skipped,
        "rows_written": len(rows),
        "output_file": output_file
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract flattened rows from LinkedIn Sales Navigator JSON files into a CSV."
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
    args = parser.parse_args()

    convert_json_to_csv(args.pattern, args.output, args.input_dir)
