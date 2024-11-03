# src/wallet/key_management.py

import os
import json
import hashlib
import secrets
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class KeyManager:
    def __init__(self, key_file='keys.json'):
        self.key_file = key_file
        self.keys = self.load_keys()

    def generate_key_pair(self):
        """Generate a new RSA key pair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def save_key_pair(self, private_key, public_key, alias):
        """Save the key pair to a file."""
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        self.keys[alias] = {
            'private_key': private_pem.decode('utf-8'),
            'public_key': public_pem.decode('utf-8')
        }
        self.save_keys()

    def load_keys(self):
        """Load keys from a JSON file."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'r') as f:
                return json.load(f)
        return {}

    def save_keys(self):
        """Save keys to a JSON file."""
        with open(self.key_file, 'w') as f:
            json.dump(self.keys, f)

    def get_private_key(self, alias):
        """Retrieve a private key by alias."""
        return self.keys.get(alias, {}).get('private_key')

    def get_public_key(self, alias):
        """Retrieve a public key by alias."""
        return self.keys.get(alias, {}).get('public_key')

    def delete_key(self, alias):
        """Delete a key by alias."""
        if alias in self.keys:
            del self.keys[alias]
            self.save_keys()
