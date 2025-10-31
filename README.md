# Data Extraction Tools

A comprehensive Python library for data manipulation, conversion, and combination. Built with best practices including robust error handling, progress tracking, and comprehensive logging.

## ✨ Key Features

- 🔄 **Smart Data Combining** - Merge multiple JSON files with validation and error recovery
- 📊 **Format Conversion** - Convert LinkedIn Sales Navigator data to CSV
- 🛡️ **Robust Error Handling** - Comprehensive error catching and recovery
- 📝 **Rich Logging** - Detailed operation logs with customizable verbosity
- 📈 **Progress Tracking** - Real-time progress bars for long operations
- 🔒 **Data Protection** - Built-in .gitignore to prevent accidental data commits
- 🧪 **Well Tested** - Unit tests for core functionality
- 📚 **Comprehensive Docs** - Detailed guides and examples

## 📁 Project Structure

```
data-extraction/
├── src/                    # Core library
│   ├── combiners/         # JSON file combining tools
│   │   └── json_combiner.py
│   ├── converters/        # Format conversion tools
│   │   ├── linkedin_json_to_csv.py
│   │   └── linkedin_json_to_csv_enhanced.py
│   └── utils/             # Utility functions
│       ├── file_utils.py       # File handling utilities
│       ├── logging_utils.py    # Logging setup and helpers
│       └── progress_utils.py   # Progress bars and spinners
├── workflows/             # Pre-built complete workflows
│   └── salesnav_workflow.py
├── examples/              # Usage examples
│   └── usage_examples.py
├── docs/                  # Documentation
│   └── SALESNAV_GUIDE.md
├── tests/                 # Unit tests
└── requirements.txt       # Dependencies (none - stdlib only!)
```

## 🚀 Core Features

### Combiners

- **JSON Combiner**: Intelligently merge multiple JSON files
  - Supports both list and object JSON formats
  - Automatic error detection and recovery
  - Handles nested data structures
  - Error handling for malformed JSON

### Converters

- **LinkedIn JSON to CSV**: Convert LinkedIn Sales Navigator data to CSV
  - Extracts company information
  - Builds LinkedIn URLs from entity URNs
  - Normalizes text and handles image artifacts
  - Processes spotlight badges

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/rahalio/data-extraction.git
cd data-extraction

# No external dependencies required - uses Python standard library only
# Python 3.8+ required
```

## 💻 Usage

### Quick Start: LinkedIn Sales Navigator Workflow

The easiest way to process LinkedIn Sales Navigator exports:

```bash
# Process all JSON files and create a CSV
python workflows/salesnav_workflow.py \
    --input-dir /path/to/json/files \
    --output-dir ./output
```

See the complete [LinkedIn Sales Navigator Guide](docs/SALESNAV_GUIDE.md) for detailed instructions.

### As a Python Module

```python
from src.combiners import combine_json_files
from src.converters import convert_json_to_csv

# Combine JSON files
result = combine_json_files(
    input_dir="./data",
    output_file="combined.json",
    pattern="*.json"
)

# Convert LinkedIn JSON to CSV
result = convert_json_to_csv(
    input_pattern="*.json",
    output_file="companies.csv",
    input_dir="./data"
)
```

### As Command-Line Tools

#### JSON Combiner

```bash
python src/combiners/json_combiner.py \
    --input-dir ./data \
    --output combined.json \
    --pattern "*.json"
```

#### LinkedIn JSON to CSV Converter

```bash
python src/converters/linkedin_json_to_csv.py \
    --pattern "*.json" \
    --output companies.csv \
    --input-dir ./data
```

## 📋 Command-Line Options

### JSON Combiner

- `--input-dir`: Directory containing JSON files (default: current directory)
- `--output`: Output filename (default: combined.json)
- `--pattern`: Glob pattern for matching files (default: \*.json)

### LinkedIn JSON to CSV

- `--pattern`: Glob pattern for input JSON files (default: \*.json)
- `--output`: Output CSV filename (default: companies.csv)
- `--input-dir`: Directory containing JSON files (default: current directory)

## 🔧 Requirements

- Python 3.8 or higher
- No external dependencies (uses Python standard library only)

## 📝 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

Repository: [https://github.com/rahalio/data-extraction](https://github.com/rahalio/data-extraction)
