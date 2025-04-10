import mnemonic  # Install using `pip install mnemonic`

# Input data to encode
input_data = "encrypted message"
print("Input:", input_data)

# Convert the input data to bytes
data_bytes = input_data.encode()

# Ensure the data length is a multiple of 4 bytes (required for BIP-39 entropy)
while len(data_bytes) % 4 != 0:
    data_bytes += b'\x00'  # Pad with null bytes if necessary

# Generate a mnemonic phrase from the data
mnemo = mnemonic.Mnemonic("english")
mnemonic_phrase = mnemo.to_mnemonic(data_bytes)
print("Mnemonic Phrase:", mnemonic_phrase)

# To reverse the process:
# Decode the mnemonic phrase back to the original data
decoded_bytes = mnemo.to_entropy(mnemonic_phrase)
decoded_data = decoded_bytes.rstrip(b'\x00').decode()  # Remove padding
print("Decoded Data:", decoded_data)



