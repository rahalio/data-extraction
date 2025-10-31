"""
Unit tests for data extraction tools

Run with: python -m pytest tests/
or: python -m unittest discover tests/
"""

import unittest
import json
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from combiners.json_combiner import combine_json_files
from converters.linkedin_json_to_csv import (
    pick_artifact_url,
    join_badges,
    normalize_text,
    build_linkedin_url
)


class TestJSONCombiner(unittest.TestCase):
    """Test cases for JSON combiner"""

    def setUp(self):
        """Create temporary directory with test files"""
        self.test_dir = tempfile.mkdtemp()

        # Create test JSON files
        test_data1 = [{"id": 1, "name": "Test1"}]
        test_data2 = [{"id": 2, "name": "Test2"}]
        test_data3 = {"id": 3, "name": "Test3"}

        with open(os.path.join(self.test_dir, "test1.json"), "w") as f:
            json.dump(test_data1, f)
        with open(os.path.join(self.test_dir, "test2.json"), "w") as f:
            json.dump(test_data2, f)
        with open(os.path.join(self.test_dir, "test3.json"), "w") as f:
            json.dump(test_data3, f)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_combine_json_files(self):
        """Test combining JSON files"""
        result = combine_json_files(
            input_dir=self.test_dir,
            output_file="combined.json"
        )

        self.assertEqual(result["files_processed"], 3)
        self.assertEqual(result["total_records"], 3)

        # Check output file
        output_path = os.path.join(self.test_dir, "combined.json")
        self.assertTrue(os.path.exists(output_path))

        with open(output_path, "r") as f:
            data = json.load(f)

        self.assertEqual(len(data), 3)


class TestLinkedInConverters(unittest.TestCase):
    """Test cases for LinkedIn converter utilities"""

    def test_normalize_text(self):
        """Test text normalization"""
        self.assertEqual(normalize_text("Hello\nWorld"), "Hello World")
        self.assertEqual(normalize_text("Multiple   spaces"), "Multiple spaces")
        self.assertEqual(normalize_text(None), "")
        self.assertEqual(normalize_text("  trim  "), "trim")

    def test_build_linkedin_url(self):
        """Test LinkedIn URL building"""
        urn = "urn:li:company:12345"
        expected = "https://www.linkedin.com/sales/company/12345"
        self.assertEqual(build_linkedin_url(urn), expected)

        self.assertEqual(build_linkedin_url(""), "")
        self.assertEqual(build_linkedin_url(None), "")

    def test_join_badges(self):
        """Test badge joining"""
        badges = [
            {"id": "badge1", "displayValue": "Value1"},
            {"id": "badge2", "displayValue": "Value2"}
        ]
        result = join_badges(badges)
        self.assertIn("badge1", result)
        self.assertIn("Value1", result)
        self.assertIn("|", result)

        self.assertEqual(join_badges(None), "")
        self.assertEqual(join_badges([]), "")

    def test_pick_artifact_url(self):
        """Test artifact URL picking"""
        pic = {
            "rootUrl": "https://example.com/",
            "artifacts": [
                {"width": 100, "fileIdentifyingUrlPathSegment": "img100.jpg"},
                {"width": 200, "fileIdentifyingUrlPathSegment": "img200.jpg"}
            ]
        }
        result = pick_artifact_url(pic, 100)
        self.assertEqual(result, "https://example.com/img100.jpg")

        self.assertEqual(pick_artifact_url(None, 100), "")


if __name__ == "__main__":
    unittest.main()
