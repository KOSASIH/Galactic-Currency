"""Galactic Currency - Neural Consensus Protocol v3.0"""
from __future__ import annotations
import hashlib, random, time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Validator:
    node_id: str; civilization: str
    stake: float; trust_score: float
    neural_weight: float; online: bool = True


@dataclass
class ConsensusVote:
    validator_id: str; block_hash: str
    approve: bool; confidence: float
    neural_embedding: List[float]; timestamp: float


@dataclass
class ConsensusResult:
    block_hash: str; approved: bool
    vote_count: int; approval_rate: float
    weighted_confidence: float; finality_time_ms: float
    consensus_round: int


class NeuralConsensusProtocol:
    VERSION = "3.0.0-neural"
    FINALITY_THRESHOLD = 0.67

    def __init__(self, attention_layers=12, attention_heads=16, min_validators=21):
        self.attention_layers = attention_layers
        self.attention_heads = attention_heads
        self.min_validators = min_validators
        self._validators: Dict[str, Validator] = {}
        self._round = 0

    def register_validator(self, v: Validator): self._validators[v.node_id] = v
    def _active(self) -> List[Validator]: return [v for v in self._validators.values() if v.online]

    def _attention_score(self, v: Validator, data: bytes) -> float:
        seed = int(hashlib.md5(v.node_id.encode() + data[:8]).hexdigest(), 16)
        random.seed(seed)
        heads = [random.gauss(v.trust_score, 0.05) for _ in range(self.attention_heads)]
        return max(0.0, min(1.0, sum(heads)/self.attention_heads))

    def _embed(self, data: bytes) -> List[float]:
        h = hashlib.sha3_256(data).digest()
        return [(b/255.0*2-1) for b in h[:16]]

    def run_consensus(self, block_hash: str, block_data: bytes) -> ConsensusResult:
        self._round += 1
        t0 = time.perf_counter()
        active = self._active()
        if len(active) < self.min_validators:
            raise RuntimeError(f"Insufficient validators: {len(active)} < {self.min_validators}")
        votes = []
        for v in active:
            attn = self._attention_score(v, block_data)
            approve = attn * v.neural_weight * v.stake > 0.5
            votes.append(ConsensusVote(v.node_id, block_hash, approve, attn, self._embed(block_data), time.time()))
        approvals = [v for v in votes if v.approve]
        total_stake = sum(self._validators[v.validator_id].stake for v in votes)
        appr_stake = sum(self._validators[v.validator_id].stake for v in approvals)
        wconf = appr_stake / max(total_stake, 1e-9)
        approved = wconf >= self.FINALITY_THRESHOLD and len(approvals) >= self.min_validators
        for vote in votes:
            vv = self._validators[vote.validator_id]
            vv.neural_weight = max(0.0, min(2.0, vv.neural_weight +
                                            0.001 * (1.0 if vote.approve == approved else -1.0)))
        return ConsensusResult(block_hash, approved, len(votes),
                               len(approvals)/len(votes), round(wconf,6),
                               round((time.perf_counter()-t0)*1000,3), self._round)

    def status(self) -> Dict[str,Any]:
        return {"version": self.VERSION, "attention_layers": self.attention_layers,
                "attention_heads": self.attention_heads,
                "registered_validators": len(self._validators),
                "active_validators": len(self._active()),
                "consensus_round": self._round,
                "finality_threshold": self.FINALITY_THRESHOLD}
