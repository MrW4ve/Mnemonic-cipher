import mnemonic  # Install using `pip install mnemonic`
import pyperclip  # Install using `pip install pyperclip`
import random  # Add this import for generating random chunk sizes

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

def encode_data(input_data, keyword):
    # Encrypt the input data using Vigenère Cipher
    encrypted_data = vigenere_cipher_encrypt(input_data, keyword)
    print("Encrypted Data:", encrypted_data)

    # Convert the encrypted data to bytes
    data_bytes = encrypted_data.encode()

    mnemo = mnemonic.Mnemonic("english")

    # Ensure the data is split into chunks of random valid lengths for BIP-39 entropy
    valid_lengths = [16, 20, 24, 28, 32]
    chunks = []
    i = 0

    while i < len(data_bytes):
        # Randomly select a valid chunk size
        chunk_size = random.choice(valid_lengths)
        chunks.append(data_bytes[i:i + chunk_size])
        i += chunk_size

    # Pad the last chunk if necessary
    if len(chunks[-1]) not in valid_lengths:
        while len(chunks[-1]) not in valid_lengths:
            chunks[-1] += b'\x00'  # Pad with null bytes

    # Generate a mnemonic phrase for each chunk
    mnemonic_phrases = [mnemo.to_mnemonic(chunk) for chunk in chunks]
    mnemonic_output = ', '.join(mnemonic_phrases)
    print("Mnemonic Phrases:", mnemonic_output)

    # Copy the mnemonic phrases to the clipboard
    pyperclip.copy(mnemonic_output)
    print("Mnemonic phrases have been copied to the clipboard.")
    return mnemonic_phrases

def decode_data(mnemonic_phrases, keyword):
    mnemo = mnemonic.Mnemonic("english")

    # Clean up the mnemonic phrases
    mnemonic_phrases = [phrase.strip().strip("'") for phrase in mnemonic_phrases]

    # Decode each mnemonic phrase back to the original data
    decoded_chunks = [mnemo.to_entropy(phrase) for phrase in mnemonic_phrases]
    decoded_data = b''.join(decoded_chunks).rstrip(b'\x00').decode()  # Remove padding

    # Decrypt the data using Vigenère Cipher
    decrypted_data = vigenere_cipher_decrypt(decoded_data, keyword)
    print("Decrypted Data:", decrypted_data)

    # Copy the decrypted data to the clipboard
    pyperclip.copy(decrypted_data)
    print("Decrypted data has been copied to the clipboard.")
    return decrypted_data

# Main program
choice = input("Do you want to encode or decode? (e/d): ").strip().lower()

if choice == 'e':
    input_data = input("Enter the data to encode: ")
    keyword = input("Enter the keyword for Vigenère Cipher: ")
    encode_data(input_data, keyword)
elif choice == 'd':
    mnemonic_phrases = input("Enter the mnemonic phrases separated by commas: ").split(',')
    keyword = input("Enter the keyword for Vigenère Cipher: ")
    decode_data(mnemonic_phrases, keyword)
else:
    print("Invalid choice. Please enter 'e' to encode or 'd' to decode.")
