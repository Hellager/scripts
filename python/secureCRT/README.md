# SecureCRT Password Decryption Tool

A Python tool for decrypting passwords stored in SecureCRT session configuration files.

## Features

- Search for configuration files by hostname
 Support for two SecureCRT password encryption methods:
 - Legacy encryption (Blowfish CBC)
 - V2 encryption (AES CBC)
 Automatic location of SecureCRT configuration directory
 Interactive user interface

## Requirements

- Python 3.x
- pycryptodome library

## Installation

```bash
pip install pycryptodome
```

## Usage

1. Run the script:

```bash
python cipher.py
```

2. Enter the hostname to search for when prompted
3. Select the configuration file to process from the search results
4. View the decrypted password

## Notes

- Windows systems only
- Requires access permission to SecureCRT configuration directory
- Default configuration path: `%APPDATA%\VanDyke\Config\Sessions`

## Technical Details

The tool supports two decryption methods:

1. Legacy Encryption (SecureCRTCrypto):
  - Uses Blowfish CBC mode
  - Uses fixed key pairs
  - UTF-16LE encoding

2. V2 Encryption (SecureCRTCryptoV2):
  - Uses AES CBC mode
  - Supports Config Passphrase
  - UTF-8 encoding
  - Includes password length and SHA256 verification

## References

- [SecureCRT Password Encryption Algorithm Analysis](https://blog.csdn.net/ly4983/article/details/131528552)

## Disclaimer

This tool is intended for legitimate configuration file recovery purposes only. Users must ensure compliance with relevant laws, regulations, and software usage agreements.

## License

MIT License