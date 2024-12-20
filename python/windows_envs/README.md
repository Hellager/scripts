# Windows Environment Variables Comparison Tool

A Python tool for exporting and comparing Windows environment variables across different hosts.

## Features

- Export local Windows environment variables to CSV
- Compare environment variables between different hosts
- Track changes in environment variables over time
- Support for multiple host comparisons

## Requirements

- Python 3.6+
- pandas
- csv module (built-in)
- socket module (built-in)

## Installation

1. Clone this repository
2. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script using Python:

```bash
python environments.py
```

The tool provides three options:
1. Export local environment variables
2. Compare host environment variables
3. Exit

## Output

The tool generates a CSV file named `windows_environment.csv` containing:
- Hostname
- Variable name
- Variable value
- Variable type

## License

MIT License