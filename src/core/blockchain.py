import hashlib
import time
from typing import List, Dict, Any, Optional

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, transactions: List[Transaction], hash: str, nonce: int):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash
        self.nonce = nonce

    @staticmethod
    def calculate_hash(index: int, previous_hash: str, timestamp: float, transactions: List[Transaction], nonce: int) -> str:
        transaction_data = ''.join([str(tx.to_dict()) for tx in transactions]).encode()
        value = f"{index}{previous_hash}{timestamp}{transaction_data}{nonce}".encode()
        return hashlib.sha256(value).hexdigest()

class MerkleTree:
    def __init__(self, transactions: List[Transaction]):
        self.transactions = transactions
        self.root = self.build_tree(transactions)

    def build_tree(self, transactions: List[Transaction]) -> str:
        if not transactions:
            return ''
        if len(transactions) == 1:
            return self.hash_transaction(transactions[0])

        new_level = []
        for i in range(0, len(transactions), 2):
            left = self.hash_transaction(transactions[i])
            right = self.hash_transaction(transactions[i + 1]) if i + 1 < len(transactions) else left
            new_level.append(self.hash_pair(left, right))
        return self.build_tree(new_level)

    @staticmethod
    def hash_transaction(transaction: Transaction) -> str:
        return hashlib.sha256(str(transaction.to_dict()).encode()).hexdigest()

    @staticmethod
    def hash_pair(left: str, right: str) -> str:
        return hashlib.sha256((left + right).encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Transaction] = []
        self.difficulty = 2  # Difficulty for PoW
        self.mining_reward = 1.0  # Reward for mining a block
        self.create_block(previous_hash='0', nonce=0)  # Genesis block

    def create_block(self, transactions: List[Transaction], previous_hash: str, nonce: int) -> Block:
        index = len(self.chain)
        timestamp = time.time()
        hash = Block.calculate_hash(index, previous_hash, timestamp, transactions, nonce)
        block = Block(index, previous_hash, timestamp, transactions, hash, nonce)
        self.chain.append(block)
        self.current_transactions = []  # Clear the current transactions
        return block

    def add_transaction(self, transaction: Transaction) -> None:
        if self.validate_transaction(transaction):
            self.current_transactions.append(transaction)

    def validate_transaction(self, transaction: Transaction) -> bool:
        # Basic validation (e.g., check if sender has enough balance)
        # In a real implementation, you would check against the blockchain
        return transaction.amount > 0

    def mine_block(self, miner_address: str) -> Block:
        # Create a new block with the current transactions
        merkle_tree = MerkleTree(self.current_transactions)
        previous_block = self.get_latest_block()
        previous_hash = previous_block.hash
        nonce = self.proof_of_work(previous_hash, merkle_tree.root)

        # Reward the miner
        self.add_transaction(Transaction(sender="0", recipient=miner_address, amount=self.mining_reward))
        return self.create_block(self.current_transactions, previous_hash, nonce)

    def proof_of_work(self, previous_hash: str, merkle_root: str) -> int:
        nonce = 0
        while True:
            hash = Block.calculate_hash(len(self.chain), previous_hash, time.time(), self.current_transactions, nonce)
            if self.is_valid_proof(hash, self.difficulty):
                return nonce
            nonce += 1

    @staticmethod
    def is_valid_proof(hash: str, difficulty: int) -> bool:
        return hash[:difficulty] == '0' * difficulty

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != Block.calculate_hash(current.index, previous.hash, current.timestamp, current.transactions, current.nonce):
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def adjust_difficulty(self) -> None:
        if len(self.chain) < 2:
            return

        latest_block = self.get_latest_block()
        previous_block = self.chain[-2]
        time_taken = latest_block.timestamp - previous_block.timestamp

        if time_taken < 30:  # If the block was mined too quickly
            self.difficulty += 1
        elif time_taken > 60:  # If the block was mined too slowly
            self.difficulty -= 1

        if self.difficulty < 1:
            self.difficulty = 1

    def execute_smart_contract(self, contract_code: str, inputs: List[Any]) -> Any:
        # Basic smart contract execution (e.g., using a Python interpreter)
        # In a real implementation, you would use a more secure and efficient approach
        exec(contract_code)
        return locals()["contract"](inputs)

    def log_event(self, event: str) -> None:
        print(f"Event: {event}")
