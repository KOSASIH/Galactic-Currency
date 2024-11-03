# examples/simple_wallet.py

import uuid

class SimpleWallet:
    def __init__(self):
        self.balance = 0.0
        self.address = self.generate_address()

    def generate_address(self):
        """Generate a unique wallet address."""
        return str(uuid.uuid4())

    def deposit(self, amount):
        """Deposit an amount into the wallet."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        print(f"Deposited: ${amount:.2f}. New balance: ${self.balance:.2f}")

    def withdraw(self, amount):
        """Withdraw an amount from the wallet."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        print(f"Withdrew: ${amount:.2f}. New balance: ${self.balance:.2f}")

    def get_balance(self):
        """Return the current balance."""
        return self.balance

    def get_address(self):
        """Return the wallet address."""
        return self.address

def main():
    wallet = SimpleWallet()
    print(f"Wallet Address: {wallet.get_address()}")
    
    # Example transactions
    wallet.deposit(100.0)
    wallet.withdraw(30.0)
    print(f"Final Balance: ${wallet.get_balance():.2f}")

if __name__ == "__main__":
    main()
