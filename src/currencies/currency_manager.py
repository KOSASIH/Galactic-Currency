"""Galactic Currency - Currency Manager v3.0"""
from __future__ import annotations
import random, time
from typing import Any, Dict, List, Optional
from .galactic_currencies import GALACTIC_CURRENCIES


class GalacticCurrencyManager:
    VERSION = "3.0.0"

    def __init__(self):
        self._currencies = GALACTIC_CURRENCIES
        self._prices: Dict[str, float] = {}
        self._refresh_prices()

    def _refresh_prices(self):
        for i, c in enumerate(self._currencies):
            random.seed(i + 1)
            self._prices[c["symbol"]] = round(random.uniform(0.001, 10_000.0), 6)
        self._last_refresh = time.time()

    def get(self, symbol: str) -> Optional[Dict[str, Any]]:
        for c in self._currencies:
            if c["symbol"] == symbol:
                p = self._prices.get(symbol, 1.0)
                return {**c, "price_gcu": p,
                        "market_cap_gcu": p * c.get("total_supply", 1e9),
                        "volume_24h_gcu": p * random.uniform(1e4, 1e8),
                        "change_24h_pct": random.gauss(0, 3)}
        return None

    def list_all(self, category=None) -> List[Dict[str, Any]]:
        return [{**c, "price_gcu": self._prices.get(c["symbol"], 1.0)}
                for c in self._currencies if not category or c.get("category") == category]

    def exchange_rate(self, from_sym: str, to_sym: str) -> float:
        fp = self._prices.get(from_sym, 1.0); tp = self._prices.get(to_sym, 1.0)
        return fp / max(tp, 1e-18)

    def convert(self, amount: float, from_sym: str, to_sym: str) -> float:
        return amount * self.exchange_rate(from_sym, to_sym)

    def top_by_market_cap(self, n: int = 10) -> List[Dict[str, Any]]:
        return sorted(self.list_all(), key=lambda x: x["price_gcu"] *
                      x.get("total_supply", 1e9), reverse=True)[:n]

    def search(self, q: str) -> List[Dict[str, Any]]:
        q = q.lower()
        return [c for c in self.list_all()
                if q in c["symbol"].lower() or q in c["name"].lower()
                or q in c.get("civilization","").lower()]

    def status(self) -> Dict[str, Any]:
        return {"version": self.VERSION, "total_currencies": len(self._currencies),
                "last_refresh": self._last_refresh,
                "categories": list({c.get("category","other") for c in self._currencies})}
