"""
Galactic Currency - Live Price Oracle v3.1
============================================
Anchors a subset of Galactic Currencies to real-world crypto market data
(via CoinGecko's public API) so price feeds are grounded in live figures
instead of purely synthetic randomness.

Author: KOSASIH | AetherNova Forge | OmniGenesis AI
"""
from __future__ import annotations
import time
from typing import Any, Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError
import json

COINGECKO_MARKETS_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd&order=market_cap_desc&per_page={n}&page=1&sparkline=false"
)

# Maps a galactic currency symbol to the real-world coin it is "anchored" to.
# The galactic token's GCU price is derived proportionally from the anchor's
# USD price, scaled by a fixed multiplier that reflects its in-universe lore.
ANCHOR_MAP: Dict[str, Dict[str, Any]] = {
    "GCU":  {"coingecko_id": "bitcoin",   "scale": 1 / 60000},
    "ARC":  {"coingecko_id": "ethereum",  "scale": 1 / 40},
    "NEX":  {"coingecko_id": "solana",    "scale": 1 / 8},
    "FLUX": {"coingecko_id": "binancecoin", "scale": 1 / 4.5},
    "QBT":  {"coingecko_id": "cardano",   "scale": 1000},
    "DRK":  {"coingecko_id": "polkadot",  "scale": 1000},
    "PSI":  {"coingecko_id": "chainlink", "scale": 1},
    "NEU":  {"coingecko_id": "avalanche-2", "scale": 1},
}

_CACHE: Dict[str, Any] = {"data": None, "fetched_at": 0.0}
_CACHE_TTL_SECONDS = 300  # 5 minutes


def _fetch_market_data(n: int = 50, timeout: int = 10) -> Optional[List[Dict[str, Any]]]:
    """Fetch top-N coins by market cap from CoinGecko's public API."""
    url = COINGECKO_MARKETS_URL.format(n=n)
    try:
        req = Request(url, headers={"User-Agent": "GalacticCurrency/3.1"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, TimeoutError, ValueError):
        return None


def get_live_market_data(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """Return cached (or freshly fetched) CoinGecko market data."""
    now = time.time()
    if not force_refresh and _CACHE["data"] and (now - _CACHE["fetched_at"] < _CACHE_TTL_SECONDS):
        return _CACHE["data"]

    data = _fetch_market_data()
    if data:
        _CACHE["data"] = data
        _CACHE["fetched_at"] = now
        return data
    # Fall back to stale cache if the live fetch fails
    return _CACHE["data"] or []


def get_anchored_price(symbol: str) -> Optional[Dict[str, Any]]:
    """Return the live-anchored GCU price for a galactic currency symbol."""
    anchor = ANCHOR_MAP.get(symbol.upper())
    if not anchor:
        return None

    market = get_live_market_data()
    coin = next((c for c in market if c.get("id") == anchor["coingecko_id"]), None)
    if not coin:
        return None

    usd_price = coin.get("current_price", 0.0)
    gcu_price = round(usd_price * anchor["scale"], 8)

    return {
        "symbol": symbol.upper(),
        "anchor_coin": coin.get("name"),
        "anchor_symbol": coin.get("symbol", "").upper(),
        "anchor_usd_price": usd_price,
        "live_price_gcu": gcu_price,
        "change_24h_pct": coin.get("price_change_percentage_24h"),
        "market_cap_usd": coin.get("market_cap"),
        "last_updated": coin.get("last_updated"),
        "source": "coingecko",
    }


def get_all_anchored_prices() -> List[Dict[str, Any]]:
    """Return live-anchored prices for every mapped galactic currency."""
    results = []
    for sym in ANCHOR_MAP:
        p = get_anchored_price(sym)
        if p:
            results.append(p)
    return results


def oracle_status() -> Dict[str, Any]:
    cached = _CACHE["data"] is not None
    age = time.time() - _CACHE["fetched_at"] if cached else None
    return {
        "version": "3.1.0-live-oracle",
        "anchored_currencies": list(ANCHOR_MAP.keys()),
        "cache_populated": cached,
        "cache_age_seconds": round(age, 1) if age is not None else None,
        "cache_ttl_seconds": _CACHE_TTL_SECONDS,
        "data_source": "CoinGecko public API (no auth required)",
    }
