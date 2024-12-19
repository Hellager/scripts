# Windows Installed Programs Tool

A Python tool for managing and comparing installed programs across different Windows hosts.

## Features

- Get installed programs information from current host
- Compare installed programs between different hosts
- Support for both single host and multi-host comparison modes
- Export results to CSV format
- Progress bar display for long operations
- Interactive command-line interface

## Requirements

- Python 3.x
- Required packages:
  - wmi
  - tqdm

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python installed.py
```

2. Select operation mode:
   - Mode 1: Get current host program information
   - Mode 2: Compare different hosts program information
   - Mode 3: Exit

3. Follow the interactive prompts to complete the operation

## Output Files

- Single host mode: `installed_programs_YYYYMMDD.csv`
- Compare mode: `compare_result_[common/different]_YYYYMMDD_HHMMSS.csv`

## License

MIT License

## Author

Stein Gu