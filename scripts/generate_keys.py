# scripts/generate_keys.py

import os
from Crypto.PublicKey import RSA

def generate_rsa_keypair(key_size=2048):
    """Generate an RSA key pair."""
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_keys(private_key, public_key):
    """Save the keys to files."""
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_key)
    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_key)

def main():
    private_key, public_key = generate_rsa_keypair()
    save_keys(private_key, public_key)
    print("RSA key pair generated and saved as 'private_key.pem' and 'public_key.pem'.")

if __name__ == "__main__":
    main()
