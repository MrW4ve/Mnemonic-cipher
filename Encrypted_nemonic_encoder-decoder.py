import mnemonic  # Install using `pip install mnemonic`
import pyperclip  # Install using `pip install pyperclip`
import random  # Add this import for generating random chunk sizes
import base64  # Add this import for Base64 encoding/decoding
import hashlib  # For deriving a salt

def vigenere_cipher_encrypt(text, key):
    # Vigenère Cipher encryption logic
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.upper()
    key = key.upper()
    encrypted_text = ""

    key_index = 0
    for char in text:
        if char in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            encrypted_char = alphabet[(alphabet.index(char) + shift) % len(alphabet)]
            encrypted_text += encrypted_char
            key_index += 1
        else:
            encrypted_text += char  # Keep non-alphabet characters as is

    return encrypted_text

def vigenere_cipher_decrypt(text, key):
    # Vigenère Cipher decryption logic
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.upper()
    key = key.upper()
    decrypted_text = ""

    key_index = 0
    for char in text:
        if char in alphabet:
            shift = alphabet.index(key[key_index % len(key)])
            decrypted_char = alphabet[(alphabet.index(char) - shift) % len(alphabet)]
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char  # Keep non-alphabet characters as is

    return decrypted_text

def binary_xor_encrypt(data, keyword):
    """
    Encrypts the data at the binary level using XOR with the keyword.
    """
    keyword_bytes = keyword.encode()  # Convert the keyword to bytes
    encrypted_data = bytearray()

    for i, byte in enumerate(data):
        # XOR each byte of the data with the corresponding byte of the keyword (cyclically)
        encrypted_data.append(byte ^ keyword_bytes[i % len(keyword_bytes)])

    return bytes(encrypted_data)

def binary_xor_decrypt(data, keyword):
    """
    Decrypts the data at the binary level using XOR with the keyword.
    (Encryption and decryption are symmetric for XOR.)
    """
    return binary_xor_encrypt(data, keyword)  # XOR decryption is the same as encryption

def derive_salt(keyword):
    """
    Derives a salt from the keyword using a hash function.
    """
    return hashlib.sha256(keyword.encode()).digest()[:4]  # Use the first 4 bytes as the salt

def encode_data(input_data, keyword):
    mnemo = mnemonic.Mnemonic("english")

    # Encrypt the input data using Vigenère Cipher
    encrypted_data = vigenere_cipher_encrypt(input_data, keyword)

    # Convert the encrypted data to bytes
    data_bytes = encrypted_data.encode()

    # Further encrypt the data at the binary level using XOR
    binary_encrypted_data = binary_xor_encrypt(data_bytes, keyword)

    # Derive a salt from the keyword
    salt = derive_salt(keyword)

    # Prepend the salt to the binary encrypted data
    binary_encrypted_data = salt + binary_encrypted_data

    # Encode binary data to Base64 for safe text representation
    binary_encrypted_data = base64.b64encode(binary_encrypted_data)

    # Ensure the data is split into chunks of random valid lengths for BIP-39 entropy
    valid_lengths = [16, 20, 24, 28, 32]
    chunks = []
    i = 0

    while i < len(binary_encrypted_data):
        chunk_size = random.choice(valid_lengths)
        chunks.append(binary_encrypted_data[i:i + chunk_size])
        i += chunk_size

    # Pad the last chunk if necessary
    if len(chunks[-1]) not in valid_lengths:
        while len(chunks[-1]) not in valid_lengths:
            chunks[-1] += bytes([random.randint(1, 255)])

    # Generate a mnemonic phrase for each chunk
    mnemonic_phrases = [mnemo.to_mnemonic(chunk) for chunk in chunks]
    current_data = ', '.join(mnemonic_phrases)

    print("Final Mnemonic Phrases:", current_data)
    pyperclip.copy(current_data)
    print("Mnemonic phrases have been copied to the clipboard.")
    return current_data


def decode_data(mnemonic_phrases, keyword):
    mnemo = mnemonic.Mnemonic("english")

    # Clean up the mnemonic phrases
    mnemonic_phrases = [phrase.strip().strip("'") for phrase in mnemonic_phrases.split(',')]

    # Decode each mnemonic phrase back to the original data
    decoded_chunks = [mnemo.to_entropy(phrase) for phrase in mnemonic_phrases]

    # Remove padding by trimming extra bytes added during encoding
    binary_encrypted_data = b''.join(decoded_chunks)

    # Decode Base64 to binary data
    try:
        binary_encrypted_data = base64.b64decode(binary_encrypted_data)
    except Exception as e:
        print("Decoding complete or error occurred:", e)
        return None

    # Derive the salt from the keyword
    salt = derive_salt(keyword)

    # Verify and remove the salt
    if binary_encrypted_data.startswith(salt):
        binary_encrypted_data = binary_encrypted_data[len(salt):]
    else:
        print("Error: Salt mismatch!")
        return None

    # Decrypt the data at the binary level using XOR
    data_bytes = binary_xor_decrypt(binary_encrypted_data, keyword)

    # Decrypt the data using Vigenère Cipher
    try:
        current_data = vigenere_cipher_decrypt(data_bytes.decode('utf-8', errors='ignore'), keyword)
    except UnicodeDecodeError as e:
        print(f"Error decoding data: {e}")
        return None

    print("Final Decoded Data:", current_data)
    pyperclip.copy(current_data)
    print("Decrypted data has been copied to the clipboard.")
    return current_data


# Main program
choice = input("Do you want to encode or decode? (e/d): ").strip().lower()

if choice == 'e':
    input_data = input("Enter the data to encode: ")
    keyword = input("Enter the keyword for the cipher: ")
    encode_data(input_data, keyword)
elif choice == 'd':
    mnemonic_phrases = input("Enter the mnemonic phrases separated by commas: ")
    keyword = input("Enter the keyword for the cipher: ")
    decode_data(mnemonic_phrases, keyword)
else:
    print("Invalid choice. Please enter 'e' to encode or 'd' to decode.")