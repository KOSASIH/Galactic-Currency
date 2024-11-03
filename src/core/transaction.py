import hashlib
import time
from typing import List, Dict, Any, Optional
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, signature: Optional[str] = None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = signature

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }

    def sign_transaction(self, private_key: SigningKey) -> None:
        if self.sender is None:
            raise Exception("Transaction must have a sender")
        message = self.sender + self.recipient + str(self.amount) + str(self.timestamp)
        self.signature = private_key.sign(message.encode()).hex()

    def is_valid(self) -> bool:
        if self.signature is None:
            return False
        public_key = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)
        message = self.sender + self.recipient + str(self.amount) + str(self.timestamp)
        return public_key.verify(bytes.fromhex(self.signature), message.encode())

class TransactionPool:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        if self.validate_transaction(transaction):
            self.transactions.append(transaction)
            self.log_event(f"Transaction added: {transaction.to_dict()}")

    def validate_transaction(self, transaction: Transaction) -> bool:
        # Basic validation (e.g., check if sender has enough balance)
        # In a real implementation, you would check against the blockchain
        if transaction.amount <= 0:
            self.log_event("Invalid transaction amount")
            return False
        if not transaction.is_valid():
            self.log_event("Invalid transaction signature")
            return False
        return True

    def clear_transactions(self) -> List[Transaction]:
        transactions_to_return = self.transactions.copy()
        self.transactions.clear()
        return transactions_to_return

    def log_event(self, event: str) -> None:
        print(f"Event: {event}")

# Example usage of the Transaction class
if __name__ == "__main__":
    # Generate a new key pair for demonstration
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    # Create a transaction
    tx = Transaction(sender=public_key.to_string().hex(), recipient="recipient_address", amount=10.0)
    tx.sign_transaction(private_key)

    # Validate the transaction
    if tx.is_valid():
        print("Transaction is valid.")
    else:
        print("Transaction is invalid.")
