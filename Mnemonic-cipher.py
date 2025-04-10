import mnemonic  # Install using `pip install mnemonic`

# Input data to encode
input_data = ("This is a test string for mnemonic encoding. ")

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

# To reverse the process:
# Decode each mnemonic phrase back to the original data
decoded_chunks = [mnemo.to_entropy(phrase) for phrase in mnemonic_phrases]
decoded_data = b''.join(decoded_chunks).rstrip(b'\x00').decode()  # Remove padding
print("Decoded Data:", decoded_data)



