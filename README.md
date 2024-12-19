# scripts
Scripts collections for various usage

## Python Scripts

### SecureCRT Tools
**Location**: `python/secureCRT/`
- `cipher.py`: SecureCRT session password decryption tool
  - Supports both legacy (Blowfish) and V2 (AES) encryption
  - Auto-detects SecureCRT config directory
  - Interactive CLI interface

### Windows System Tools
**Location**: `python/windows_installed/`
- `installed.py`: Windows installed programs management tool
  - Lists all installed programs on Windows systems
  - Compares installed programs across different hosts
  - Exports results to CSV format
  - Features progress bar and interactive CLI

## Directory Structure
```
scripts/
├── python/
│   ├── secureCRT/
│   │   ├── cipher.py
│   │   ├── README.md
│   │   ├── README_CN.md
│   │   └── requirements.txt
│   └── windows_installed/
│       ├── installed.py
│       ├── README.md
│       ├── README_CN.md
│       └── requirements.txt
└── README.md
```

## Usage
Each script has its own README file with detailed usage instructions. Please refer to the specific script's directory for more information.

## Requirements
Dependencies are managed separately for each script. Check the `requirements.txt` file in each script's directory for specific requirements.

## License
MIT License
