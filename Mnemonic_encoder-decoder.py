import mnemonic  # Install using `pip install mnemonic`

def encode_data(input_data):
    # Convert the input data to bytes
    data_bytes = input_data.encode()

    mnemo = mnemonic.Mnemonic("english")

    # Ensure the data is split into chunks of valid lengths for BIP-39 entropy
    valid_lengths = [16, 20, 24, 28, 32]
    max_length = max(valid_lengths)

    # Split the data into chunks of valid lengths
    chunks = [data_bytes[i:i + max_length] for i in range(0, len(data_bytes), max_length)]

    # Pad the last chunk if necessary
    if len(chunks[-1]) not in valid_lengths:
        while len(chunks[-1]) not in valid_lengths:
            chunks[-1] += b'\x00'  # Pad with null bytes

    # Generate a mnemonic phrase for each chunk
    mnemonic_phrases = [mnemo.to_mnemonic(chunk) for chunk in chunks]
    print("Mnemonic Phrases:", mnemonic_phrases)
    # Print the entropy data in binary for each chunk
    for chunk in chunks:
        print("Entropy (binary):", ''.join(format(byte, '08b') for byte in chunk))
    return mnemonic_phrases

def decode_data(mnemonic_phrases):
    mnemo = mnemonic.Mnemonic("english")

    # Decode each mnemonic phrase back to the original data
    decoded_chunks = [mnemo.to_entropy(phrase) for phrase in mnemonic_phrases]
    decoded_data = b''.join(decoded_chunks).rstrip(b'\x00').decode()  # Remove padding
    print("Decoded Data:", decoded_data)
    return decoded_data

# Main program
choice = input("Do you want to encode or decode? (e/d): ").strip().lower()

if choice == 'e':
    input_data = input("Enter the data to encode: ")
    encode_data(input_data)
elif choice == 'd':
    mnemonic_phrases = input("Enter the mnemonic phrases separated by commas: ").split(',')
    decode_data(mnemonic_phrases)
else:
    print("Invalid choice. Please enter 'e' to encode or 'd' to decode.")


# Note: This code uses the BIP-39 standard for mnemonic phrases. The input data is split into chunks of valid lengths for BIP-39 entropy.
# The mnemonic phrases are generated for each chunk, and the original data can be reconstructed from the mnemonic phrases.

# This code was created for educational purposes and used github copilot [gen-AI] to assist in writing the code.
