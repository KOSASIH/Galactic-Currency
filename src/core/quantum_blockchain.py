"""Galactic Currency - Quantum-Enhanced Blockchain v3.0"""
from __future__ import annotations
import hashlib, json, time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class QuantumBlock:
    index: int; timestamp: float
    transactions: List[Dict[str, Any]]
    previous_hash: str; quantum_proof: str
    neural_consensus_hash: str; dimension_anchor: str
    nonce: int = 0; hash: str = field(init=False)

    def __post_init__(self): self.hash = self._compute_hash()

    def _compute_hash(self) -> str:
        d = {"index": self.index, "timestamp": self.timestamp,
             "transactions": self.transactions, "previous_hash": self.previous_hash,
             "quantum_proof": self.quantum_proof,
             "neural_consensus_hash": self.neural_consensus_hash,
             "dimension_anchor": self.dimension_anchor, "nonce": self.nonce}
        return hashlib.sha3_512(json.dumps(d, sort_keys=True).encode()).hexdigest()

    def recompute(self): self.hash = self._compute_hash()


class QuantumBlockchain:
    VERSION = "3.0.0-quantum"

    def __init__(self, chain_id: str = "galactic-mainnet"):
        self.chain_id = chain_id
        self._chain: List[QuantumBlock] = [self._genesis()]
        self._pending: List[Dict] = []

    def _genesis(self) -> QuantumBlock:
        return QuantumBlock(0, 0.0, [], "0"*128,
                            "GENESIS_ZK_STARK", "GENESIS_NEURAL", "PRIME_DIMENSION_0")

    def _zk_proof(self, txs: List[Dict]) -> str:
        return "ZK-STARK:" + hashlib.shake_256(
            json.dumps(txs, sort_keys=True).encode()).hexdigest(32)

    def _dimension_anchor(self) -> str:
        return hashlib.sha3_256(
            f"dim:{len(self._chain)}:{time.time()}".encode()).hexdigest()[:24]

    def add_transaction(self, tx: Dict) -> int:
        self._pending.append(tx); return len(self._pending)

    def mine_block(self, neural_hash: str = "0"*64) -> QuantumBlock:
        if not self._pending: raise ValueError("No pending transactions")
        prev = self._chain[-1]
        b = QuantumBlock(len(self._chain), time.time(), self._pending.copy(),
                         prev.hash, self._zk_proof(self._pending), neural_hash,
                         self._dimension_anchor())
        self._chain.append(b); self._pending.clear(); return b

    def is_valid(self) -> bool:
        for i in range(1, len(self._chain)):
            c, p = self._chain[i], self._chain[i-1]
            if c.hash != c._compute_hash() or c.previous_hash != p.hash: return False
        return True

    @property
    def height(self) -> int: return len(self._chain) - 1

    def get_block(self, idx: int) -> Optional[QuantumBlock]:
        return self._chain[idx] if 0 <= idx < len(self._chain) else None

    def status(self) -> Dict[str, Any]:
        return {"chain_id": self.chain_id, "version": self.VERSION,
                "height": self.height, "pending": len(self._pending),
                "valid": self.is_valid(),
                "latest_hash": self._chain[-1].hash[:16] + "..."}
