# Data Storage Location

## 📍 Primary Data Directory

All extracted and processed data is stored in:

```
~/Documents/data-extraction-data/
```

## 📁 Directory Structure

```
data-extraction-data/
├── linkedin-salesnav/      # LinkedIn Sales Navigator data
│   ├── raw/               # Original JSON exports (30 files, 1.6MB)
│   ├── processed/         # Generated CSV files
│   └── archives/          # Backup/historical data
│
├── apollo-io/             # Apollo.io data
│   ├── raw/              # Original exports
│   └── processed/        # Generated files
│
├── exports/              # Final deliverables
└── sample-data/          # Test data for development
```

## 🚀 Usage Examples

### Process LinkedIn SalesNav Data

```bash
# Process raw JSON files to CSV
python3 workflows/linkedin_salesnav_pipeline.py \
  --input-dir ~/Documents/data-extraction-data/linkedin-salesnav/raw \
  --output-dir ~/Documents/data-extraction-data/linkedin-salesnav/processed
```

### Combine Multiple JSON Files

```bash
python3 src/combiners/json_merger.py \
  --input-dir ~/Documents/data-extraction-data/linkedin-salesnav/raw \
  --output ~/Documents/data-extraction-data/linkedin-salesnav/processed/combined.json
```

### Convert JSON to CSV

```bash
python3 src/converters/linkedin_to_csv_enhanced.py \
  --input-dir ~/Documents/data-extraction-data/linkedin-salesnav/raw \
  --output ~/Documents/data-extraction-data/linkedin-salesnav/processed/companies.csv
```

## 🔒 Data Protection

- ✅ All real data is stored **outside** the git repository
- ✅ Protected by comprehensive `.gitignore` patterns
- ✅ No risk of accidental public commits
- ✅ Backup location: `~/Documents/data-extraction-data/linkedin-salesnav/archives/`

## 📊 Current Data Inventory

### LinkedIn Sales Navigator

- **Raw Files:** 30 JSON files
- **Total Size:** ~1.6 MB
- **Records:** 750 companies
- **Last Updated:** October 31, 2025

## 📝 Best Practices

1. **Keep raw data intact** - Always preserve original JSON files
2. **Version processed outputs** - Add dates to processed files
3. **Regular backups** - Archive important extracts
4. **Document sources** - Note where data came from and when

## 🔄 Workflow

```
Raw Data (JSON)
    ↓
[json_merger.py] → Combined JSON
    ↓
[linkedin_to_csv_enhanced.py] → Processed CSV
    ↓
Export to clients/analysis tools
```

## 💡 Tips

- Use `--verbose` flag for detailed logging
- Check the `processed/` folder before overwriting
- Archive old exports before processing new data
- Use the `--keep-combined` flag to retain intermediate files
