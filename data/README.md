# Data Directory

This directory is for storing data files during processing. **All data files are automatically ignored by git** to protect sensitive information.

## Directory Structure

```
data/
├── sample/                 # Sample/test data (safe to commit)
│   └── linkedin_salesnav/  # Sample LinkedIn Sales Navigator data
├── raw/                    # Raw input data (git-ignored)
├── processed/              # Processed output data (git-ignored)
└── exports/                # Final export files (git-ignored)
```

## Usage

### For Development/Testing

Place sample data files in `data/sample/` - these can be committed to git as examples.

### For Production Use

- Place your raw data files in `data/raw/`
- Processed files will be saved to `data/processed/`
- Final exports will be saved to `data/exports/`

All production data directories are automatically git-ignored.

## Running the Workflow

```bash
# Process data from raw directory
python3 workflows/linkedin_salesnav_pipeline.py \
    --input-dir ./data/raw/linkedin_exports \
    --output-dir ./data/processed

# Use sample data for testing
python3 workflows/linkedin_salesnav_pipeline.py \
    --input-dir ./data/sample/linkedin_salesnav \
    --output-dir ./data/processed
```

## Security

⚠️ **IMPORTANT**: Never commit real company or personal data to git!

All data directories except `sample/` are git-ignored by default. Only anonymized sample data should be placed in the `sample/` directory.
