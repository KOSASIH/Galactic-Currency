# src/wallet/wallet.py

import json
import os
from key_management import KeyManager

class Wallet:
    def __init__(self, wallet_file='wallet.json'):
        self.wallet_file = wallet_file
        self.wallet_data = self.load_wallet()

    def create_wallet(self, alias):
        """Create a new wallet with a key pair."""
        key_manager = KeyManager()
        private_key, public_key = key_manager.generate_key_pair()
        key_manager.save_key_pair(private_key, public_key, alias)

        self.wallet_data[alias] = {
            'balance': 0,
            'transactions': []
        }
        self.save_wallet()

    def load_wallet(self):
        """Load wallet data from a JSON file."""
        if os.path.exists(self.wallet_file):
            with open(self.wallet_file, 'r') as f:
                return json.load(f)
        return {}

    def save_wallet(self):
        """Save wallet data to a JSON file."""
        with open(self.wallet_file, 'w') as f:
            json.dump(self.wallet_data, f)

    def send_tokens(self, from_alias, to_alias, amount):
        """Send tokens from one wallet to another."""
        if from_alias not in self.wallet_data or to_alias not in self.wallet_data:
            raise ValueError("Invalid wallet alias.")

        if self.wallet_data[from_alias]['balance'] < amount:
            raise ValueError("Insufficient balance.")

        self.wallet_data[from_alias]['balance'] -= amount
        self.wallet_data[to_alias]['balance'] += amount

        transaction = {
            'from': from_alias,
            'to': to_alias,
            'amount': amount
 }
        self.wallet_data[from_alias]['transactions'].append(transaction)
        self.wallet_data[to_alias]['transactions'].append(transaction)

        self.save_wallet()

    def receive_tokens(self, alias, amount):
        """Receive tokens into a wallet."""
        if alias not in self.wallet_data:
            raise ValueError("Invalid wallet alias.")

        self.wallet_data[alias]['balance'] += amount
        self.save_wallet()

    def backup_wallet(self, seed_phrase):
        """Backup wallet data using a seed phrase."""
        # Implement seed phrase-based backup and recovery
        pass

    def recover_wallet(self, seed_phrase):
        """Recover a wallet using a seed phrase."""
        # Implement seed phrase-based backup and recovery
        pass
