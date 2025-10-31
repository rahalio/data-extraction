# LinkedIn Sales Navigator Data Extraction Guide

Complete guide for extracting and processing LinkedIn Sales Navigator company data.

## 📋 Quick Start

### Option 1: Using the Workflow Script (Recommended)

The easiest way to process your SalesNav exports:

```bash
cd /Users/nrahal/@code_2025/utils/data-extraction

# Process JSON files from SalesNav directory
python workflows/salesnav_workflow.py \
    --input-dir /Users/nrahal/@code_2025/utils/SalesNav/ListsExtracts/Small_Fis_GCC_Growth_100_Percent/SourceJsons \
    --output-dir ./output
```

This will:

1. ✅ Combine all JSON files
2. ✅ Convert to CSV with LinkedIn URLs
3. ✅ Clean up temporary files
4. ✅ Output `linkedin_companies.csv`

### Option 2: Step-by-Step Manual Process

#### Step 1: Combine JSON Files

```bash
python src/combiners/json_combiner.py \
    --input-dir /path/to/your/json/files \
    --output combined_salesnav.json \
    --pattern "*.json"
```

#### Step 2: Convert to CSV

```bash
python src/converters/linkedin_json_to_csv.py \
    --pattern "combined_salesnav.json" \
    --output linkedin_companies.csv \
    --input-dir /path/to/your/json/files
```

### Option 3: Using as Python Module

```python
from src.combiners import combine_json_files
from src.converters import convert_json_to_csv

# Combine
combine_json_files(
    input_dir="./SourceJsons",
    output_file="combined.json"
)

# Convert
convert_json_to_csv(
    input_pattern="combined.json",
    output_file="companies.csv",
    input_dir="./SourceJsons"
)
```

## 📊 CSV Output Fields

| Field                                | Description                                              |
| ------------------------------------ | -------------------------------------------------------- |
| `companyName`                        | Company name                                             |
| `industry`                           | Industry sector                                          |
| `employeeCountRange`                 | Employee size range (e.g., `11-50 employees`)            |
| `employeeDisplayCount`               | Displayed employee count                                 |
| `listCount`                          | Number of lists the company appears in                   |
| `saved`                              | Whether saved/bookmarked                                 |
| `entityUrn`                          | LinkedIn internal company URN                            |
| **`linkedin_url`**                   | **Public LinkedIn Sales Navigator URL** ⭐               |
| `recipeType`                         | LinkedIn metadata                                        |
| `trackingId`                         | LinkedIn tracking ID                                     |
| `description`                        | Company description (normalized to single line)          |
| `logo_100` / `logo_200` / `logo_400` | Company logos (different resolutions)                    |
| `spotlightBadges`                    | Special LinkedIn highlights (e.g., "Hiring on LinkedIn") |
| `source_file`                        | The JSON file the record came from                       |

## 🔧 Advanced Options

### Keep Intermediate Combined File

```bash
python workflows/salesnav_workflow.py \
    --input-dir ./SourceJsons \
    --output-dir ./output \
    --keep-combined
```

### Process Specific Pattern

```bash
python src/combiners/json_combiner.py \
    --input-dir ./SourceJsons \
    --output combined.json \
    --pattern "GCC-FI--s-*.json"
```

### Custom CSV Output Name

```bash
python src/converters/linkedin_json_to_csv.py \
    --pattern "combined.json" \
    --output my_companies_export.csv
```

## 📁 Recommended Directory Structure

```
your-project/
├── raw_data/
│   └── salesnav_exports/
│       ├── GCC-FI--s-100--01.json
│       ├── GCC-FI--s-100--02.json
│       └── ...
├── processed/
│   └── linkedin_companies.csv
└── archive/
    └── 2025-10-31/
        └── combined_backup.json
```

## 🚀 Complete Workflow Example

```bash
# 1. Navigate to data-extraction repo
cd /Users/nrahal/@code_2025/utils/data-extraction

# 2. Create output directory
mkdir -p output

# 3. Run the workflow
python workflows/salesnav_workflow.py \
    --input-dir /Users/nrahal/@code_2025/utils/SalesNav/ListsExtracts/Small_Fis_GCC_Growth_100_Percent/SourceJsons \
    --output-dir ./output

# 4. Open the CSV
open output/linkedin_companies.csv
```

## 📝 Notes

- **Data Safety**: All data files (JSON, CSV) are automatically excluded from git commits via `.gitignore`
- **No Dependencies**: Uses only Python standard library (3.8+)
- **Batch Processing**: Can process hundreds of JSON files efficiently
- **Error Handling**: Skips malformed files and continues processing
- **URL Building**: Automatically constructs LinkedIn Sales Navigator URLs from entity URNs

## 🔒 Data Privacy

All extracted data is protected by `.gitignore` patterns:

- `*.json` - All JSON files
- `*.csv` - All CSV files
- `*linkedin*.*` - LinkedIn-specific exports
- `*salesnav*.*` - Sales Navigator exports
- `data/`, `raw_data/`, `processed_data/` - Data directories

**No personal or company data will be committed to GitHub!**

## 🆘 Troubleshooting

### No files found

```bash
# Check your input directory path
ls /path/to/your/json/files/*.json

# Make sure you're using absolute paths or correct relative paths
```

### Import errors

```bash
# Make sure you're running from the data-extraction directory
cd /Users/nrahal/@code_2025/utils/data-extraction

# Or use absolute paths
python /Users/nrahal/@code_2025/utils/data-extraction/workflows/salesnav_workflow.py --input-dir ./data
```

### Permission errors

```bash
# Make sure the output directory is writable
chmod +w /path/to/output/directory
```

## 📧 Support

For issues or questions, please open an issue on the repository.
