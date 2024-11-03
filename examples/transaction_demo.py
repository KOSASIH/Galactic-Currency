# examples/transaction_demo.py

from simple_wallet import SimpleWallet

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def execute(self):
        """Execute the transaction."""
        if self.sender.get_balance() < self.amount:
            raise ValueError("Insufficient balance for transaction.")
        self.sender.withdraw(self.amount)
        self.receiver.deposit(self.amount)
        print(f"Transaction successful: ${self.amount:.2f} sent from {self.sender.get_address()} to {self.receiver.get_address()}.")

def main():
    # Create two wallets
    wallet1 = SimpleWallet()
    wallet2 = SimpleWallet()

    print(f"Wallet 1 Address: {wallet1.get_address()}")
    print(f"Wallet 2 Address: {wallet2.get_address()}")

    # Deposit some funds into wallet1
    wallet1.deposit(200.0)

    # Create a transaction from wallet1 to wallet2
    transaction = Transaction(sender=wallet1, receiver=wallet2, amount=50.0)

    # Execute the transaction
    try:
        transaction.execute()
    except ValueError as e:
        print(f"Transaction failed: {e}")

    # Display final balances
    print(f"Wallet 1 Final Balance: ${wallet1.get_balance():.2f}")
    print(f"Wallet 2 Final Balance: ${wallet2.get_balance():.2f}")

if __name__ == "__main__":
    main()
