import random
from typing import List, Dict, Any

class Validator:
    def __init__(self, address: str, stake: float):
        self.address = address
        self.stake = stake

class Consensus:
    def __init__(self):
        self.validators: List[Validator] = []
        self.delegations: Dict[str, List[str]] = {}  # Maps delegator addresses to their delegated validators

    def add_validator(self, address: str, stake: float) -> None:
        if self.get_validator(address) is None:
            self.validators.append(Validator(address, stake))
            self.log_event(f"Validator added: {address} with stake {stake}")
        else:
            self.update_stake(address, stake)

    def remove_validator(self, address: str) -> None:
        validator = self.get_validator(address)
        if validator:
            self.validators.remove(validator)
            self.log_event(f"Validator removed: {address}")

    def update_stake(self, address: str, stake: float) -> None:
        validator = self.get_validator(address)
        if validator:
            validator.stake += stake
            self.log_event(f"Stake updated for validator: {address} to {validator.stake}")

    def get_validator(self, address: str) -> Validator:
        for validator in self.validators:
            if validator.address == address:
                return validator
        return None

    def delegate_stake(self, delegator: str, validator_address: str) -> None:
        if self.get_validator(validator_address) is None:
            raise Exception("Validator does not exist")
        if delegator not in self.delegations:
            self.delegations[delegator] = []
        self.delegations[delegator].append(validator_address)
        self.log_event(f"{delegator} delegated stake to {validator_address}")

    def select_validator(self) -> str:
        total_stake = sum(validator.stake for validator in self.validators)
        if total_stake == 0:
            return None

        # Randomly select a validator based on their stake
        selection = random.uniform(0, total_stake)
        current = 0
        for validator in self.validators:
            current += validator.stake
            if current >= selection:
                return validator.address
        return None

    def log_event(self, event: str) -> None:
        print(f"Event: {event}")

# Example usage of the Consensus class
if __name__ == "__main__":
    consensus = Consensus()
    consensus.add_validator("validator1_address", 100)
    consensus.add_validator("validator2_address", 200)
    consensus.delegate_stake("delegator1_address", "validator1_address")

    selected_validator = consensus.select_validator()
    print(f"Selected validator: {selected_validator}")
