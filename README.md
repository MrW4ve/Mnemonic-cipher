# Mnemonic-Cipher

A Python-based encryption and decryption tool that encodes text into BIP-39 mnemonic phrases using a combination of cryptographic techniques. This project supports encoding data with a Vigenère Cipher, binary XOR encryption, and Base64 encoding, while also splitting the data into randomized BIP-39-compatible chunks for added obscurity.

## Features

- **Vigenère Cipher**: Encrypts text using a keyword-based substitution cipher.
- **Binary XOR Encryption**: Adds an additional layer of encryption at the binary level.
- **BIP-39 Mnemonic Encoding**: Converts binary data into mnemonic phrases for secure and human-readable representation.
- **Base64 Encoding**: Ensures safe text representation of binary data.
- **Salt Derivation**: Uses a hash-based salt to enhance security.
- **Randomized Chunk Sizes**: Splits data into chunks of valid BIP-39 entropy lengths (16, 20, 24, 28, 32 bytes) for data-size obscuring.

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `mnemonic` (Install using `pip install mnemonic`)
  - `pyperclip` (Install using `pip install pyperclip`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mnemonic-cipher.git
   cd mnemonic-cipher
   ```
