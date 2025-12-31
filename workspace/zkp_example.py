"""
Example: Encrypting tourist data and generating/verifying a Zero-Knowledge Proof (ZKP)
- Uses PyCryptodome for AES encryption
- Uses py-snark for ZKP (mocked, as real ZKP circuits require setup)
"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# --- Tourist Data Encryption ---
def encrypt_data(data: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_data(enc: str, key: bytes) -> str:
    raw = base64.b64decode(enc)
    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode()

# --- Mock ZKP Generation/Verification ---
def generate_zkp(sale_amount: int, commission: int) -> dict:
    # In real use, generate a ZKP attesting commission = sale_amount * rate
    return {"proof": "mock_zkp_proof", "public": {"sale_amount": sale_amount, "commission": commission}}

def verify_zkp(proof: dict) -> bool:
    # In real use, verify the ZKP
    return proof["proof"] == "mock_zkp_proof"

# --- Example Usage ---
if __name__ == "__main__":
    key = get_random_bytes(32)  # AES-256
    tourist_data = "John Doe, Passport 123456, Email: john@example.com"
    encrypted = encrypt_data(tourist_data, key)
    print("Encrypted:", encrypted)
    decrypted = decrypt_data(encrypted, key)
    print("Decrypted:", decrypted)

    # ZKP for commission
    zkp = generate_zkp(1000, 10)
    print("ZKP:", zkp)
    print("ZKP valid?", verify_zkp(zkp))
