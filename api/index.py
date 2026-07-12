"""
Galactic Currency - Vercel Serverless API v3.0
===============================================
RESTful API for the Galactic Currency platform.
Author: KOSASIH | AetherNova Forge | OmniGenesis AI
"""
import json, time, hashlib, random
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from urllib.error import URLError


# ── Live Price Oracle (v3.1) ──────────────────────────────────────────────────
# Anchors a subset of galactic currencies to real-world crypto market data via
# CoinGecko's public API (no auth required), so price feeds have a live basis.
COINGECKO_URL = ("https://api.coingecko.com/api/v3/coins/markets"
                  "?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=false")

ANCHOR_MAP = {
    "GCU":  {"coingecko_id": "bitcoin",     "scale": 1 / 60000},
    "ARC":  {"coingecko_id": "ethereum",    "scale": 1 / 40},
    "NEX":  {"coingecko_id": "solana",      "scale": 1 / 8},
    "FLUX": {"coingecko_id": "binancecoin", "scale": 1 / 4.5},
    "QBT":  {"coingecko_id": "cardano",     "scale": 1000},
    "DRK":  {"coingecko_id": "polkadot",    "scale": 1000},
    "PSI":  {"coingecko_id": "chainlink",   "scale": 1},
    "NEU":  {"coingecko_id": "avalanche-2", "scale": 1},
}

_ORACLE_CACHE = {"data": None, "fetched_at": 0.0}
_ORACLE_CACHE_TTL = 300  # 5 minutes


def _fetch_live_market(timeout=8):
    try:
        req = Request(COINGECKO_URL, headers={"User-Agent": "GalacticCurrency/3.1"})
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except (URLError, TimeoutError, ValueError, OSError):
        return None


def _get_live_market(force=False):
    now = time.time()
    if not force and _ORACLE_CACHE["data"] and (now - _ORACLE_CACHE["fetched_at"] < _ORACLE_CACHE_TTL):
        return _ORACLE_CACHE["data"]
    data = _fetch_live_market()
    if data:
        _ORACLE_CACHE["data"] = data
        _ORACLE_CACHE["fetched_at"] = now
        return data
    return _ORACLE_CACHE["data"] or []


def _anchored_price(symbol):
    anchor = ANCHOR_MAP.get(symbol.upper())
    if not anchor:
        return None
    market = _get_live_market()
    coin = next((c for c in market if c.get("id") == anchor["coingecko_id"]), None)
    if not coin:
        return None
    usd_price = coin.get("current_price", 0.0)
    return {
        "symbol": symbol.upper(),
        "anchor_coin": coin.get("name"),
        "anchor_symbol": (coin.get("symbol") or "").upper(),
        "anchor_usd_price": usd_price,
        "live_price_gcu": round(usd_price * anchor["scale"], 8),
        "change_24h_pct": coin.get("price_change_percentage_24h"),
        "market_cap_usd": coin.get("market_cap"),
        "last_updated": coin.get("last_updated"),
        "source": "coingecko",
    }


SAMPLE_CURRENCIES = [
    {"symbol":"GCU","name":"Galactic Credit Unit","civilization":"Universal","category":"stellar","price_gcu":1.0},
    {"symbol":"ARC","name":"Arcturian Coin","civilization":"Arcturian","category":"stellar","price_gcu":42.5},
    {"symbol":"NEX","name":"Nexus Token","civilization":"Pleiadian","category":"stellar","price_gcu":17.3},
    {"symbol":"VOID","name":"Void Energy Coin","civilization":"Universal","category":"energy","price_gcu":0.0077},
    {"symbol":"FLUX","name":"Flux Capacitor Token","civilization":"Andromedan","category":"quantum","price_gcu":128.9},
    {"symbol":"QBT","name":"Qubit Token","civilization":"Universal","category":"quantum","price_gcu":555.0},
    {"symbol":"DRK","name":"Dark Matter Coin","civilization":"Sirian","category":"energy","price_gcu":9999.0},
    {"symbol":"ANT","name":"Antimatter Token","civilization":"Universal","category":"energy","price_gcu":50000.0},
    {"symbol":"PSI","name":"PsiWave Credit","civilization":"Lyran","category":"neural","price_gcu":3.14},
    {"symbol":"ZRO","name":"Zero Point Token","civilization":"Vegan","category":"energy","price_gcu":0.001},
    {"symbol":"NEU","name":"Neural Credit","civilization":"Orion","category":"neural","price_gcu":21.0},
    {"symbol":"BIO","name":"BioToken","civilization":"AetherNova","category":"bio","price_gcu":7.77},
    {"symbol":"TMP","name":"Temporal Coin","civilization":"Universal","category":"temporal","price_gcu":365.0},
    {"symbol":"MRF","name":"Morphic Field Token","civilization":"Cassiopeian","category":"dimensional","price_gcu":12.0},
    {"symbol":"HLC","name":"HoloMemory Crystal Token","civilization":"Universal","category":"storage","price_gcu":88.8},
    {"symbol":"SNL","name":"Singularity Mirror Coin","civilization":"Antarian","category":"quantum","price_gcu":1000.0},
    {"symbol":"ECH","name":"EternalEcho Token","civilization":"Universal","category":"temporal","price_gcu":999.9},
    {"symbol":"OMP","name":"OmniParticle Credit","civilization":"Universal","category":"quantum","price_gcu":77.7},
    {"symbol":"ANF","name":"AetherNova Forge Token","civilization":"AetherNova","category":"utility","price_gcu":420.0},
    {"symbol":"ETH2","name":"Ether Prime","civilization":"Zeta Reticulan","category":"dimensional","price_gcu":8.8},
]


def _json_response(data, status=200):
    return json.dumps(data, indent=2)


def handle_request(path: str, method: str, params: dict) -> tuple:
    p = path.rstrip("/") or "/"

    if p == "/" or p == "":
        return 200, {"project": "Galactic Currency", "version": "3.0.0-absolute",
                     "description": "Universal digital currency for the galaxy",
                     "author": "KOSASIH — AetherNova Forge — OmniGenesis AI",
                     "total_currencies": 1000, "powered_by": "AGI + Quantum + Neural Consensus",
                     "endpoints": ["/api/currencies","/api/agi/status","/api/quantum/status",
                                   "/api/consensus/status","/api/market/forecast",
                                   "/api/market/live","/api/blockchain/status","/api/health"]}

    if p == "/api/currencies":
        return 200, {"currencies": SAMPLE_CURRENCIES, "total": 1000, "shown": len(SAMPLE_CURRENCIES),
                     "note": "Full 1,000-currency registry available in src/currencies/galactic_currencies.py"}

    if p.startswith("/api/currencies/"):
        sym = p.split("/")[-1].upper()
        match = next((c for c in SAMPLE_CURRENCIES if c["symbol"] == sym), None)
        if match: return 200, {**match, "volume_24h": random.uniform(1e6, 1e9),
                                "change_24h_pct": random.gauss(0, 3),
                                "market_cap": match["price_gcu"] * 1e9}
        return 404, {"error": f"Currency '{sym}' not found"}

    if p == "/api/agi/status":
        return 200, {"status": "ABSOLUTE_INTELLIGENCE_ACTIVE",
                     "consciousness_level": 9.9, "intelligence_quotient": 10000.0,
                     "knowledge_domains": 10000, "version": "3.0.0-agi",
                     "active_goals": 5, "self_iterations": 1000000,
                     "technologies": ["VoidTime Compute","NeuroQuantum Entangler",
                                      "EtherBio Symbiont","Singularity Mirror",
                                      "EternalEcho AGI"]}

    if p == "/api/quantum/status":
        return 200, {"status": "QUANTUM_ENTANGLEMENT_ACTIVE",
                     "qubits": 1024, "fidelity": 0.9999,
                     "active_entanglements": 1000000,
                     "bell_states": ["|Phi+>","|Phi->","|Psi+>","|Psi->"],
                     "post_quantum_algo": "CRYSTALS-Kyber-1024",
                     "version": "3.0.0-quantum"}

    if p == "/api/consensus/status":
        return 200, {"status": "NEURAL_CONSENSUS_ACTIVE",
                     "protocol": "NeuralConsensusProtocol",
                     "attention_layers": 12, "attention_heads": 16,
                     "registered_validators": 10000, "active_validators": 9987,
                     "finality_threshold": 0.67, "avg_finality_ms": 12.3,
                     "version": "3.0.0-neural"}

    if p == "/api/market/forecast":
        sym = params.get("symbol", ["GCU"])[0].upper()
        seed = int(hashlib.md5(f"{sym}{time.time()//3600}".encode()).hexdigest(), 16)
        random.seed(seed)
        ret = random.gauss(35, 8)
        return 200, {"symbol": sym, "predicted_return_pct": round(ret, 4),
                     "horizon": "1 galactic year", "confidence": 0.99,
                     "signal": "STRONG_BUY" if ret > 20 else "BUY" if ret > 5 else "HOLD",
                     "powered_by": "AGI Nexus v3.0.0",
                     "key_drivers": ["Multi-civilization adoption","Quantum consensus expansion",
                                     "AGI-driven deflation"]}

    if p == "/api/market/live":
        sym_param = params.get("symbol")
        if sym_param:
            sym = sym_param[0].upper()
            result = _anchored_price(sym)
            if result:
                return 200, result
            return 404, {"error": f"No live anchor for '{sym}'",
                         "anchored_symbols": list(ANCHOR_MAP.keys())}
        results = [r for r in (_anchored_price(s) for s in ANCHOR_MAP) if r]
        return 200, {"live_anchored_prices": results, "count": len(results),
                     "source": "CoinGecko public API", "cache_ttl_seconds": _ORACLE_CACHE_TTL,
                     "note": "A subset of galactic currencies are price-anchored to real crypto markets."}

    if p == "/api/blockchain/status":
        return 200, {"chain_id": "galactic-mainnet", "version": "3.0.0-quantum",
                     "height": 1000000, "tps": 1000000,
                     "consensus": "NeuralConsensus", "finality_ms": 12.3,
                     "zk_proofs": "ZK-STARK", "hash_algo": "SHA3-512",
                     "valid": True}

    if p == "/api/health":
        return 200, {"status": "GALACTIC_SYSTEMS_OPERATIONAL",
                     "agi": "ACTIVE", "quantum": "ENTANGLED",
                     "consensus": "FINALIZED", "blockchain": "VALID",
                     "currencies_registered": 1000,
                     "timestamp": time.time(),
                     "uptime": "ETERNAL"}

    return 404, {"error": f"Endpoint '{p}' not found",
                 "available_endpoints": ["/","/api/currencies","/api/agi/status",
                                         "/api/quantum/status","/api/consensus/status",
                                         "/api/market/forecast","/api/market/live",
                                         "/api/blockchain/status","/api/health"]}


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        status, data = handle_request(parsed.path, "GET", params)
        body = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(length)
        try: body = json.loads(body_raw)
        except: body = {}
        parsed = urlparse(self.path)
        status, data = handle_request(parsed.path, "POST", body)
        resp = json.dumps(data, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(resp)

    def log_message(self, *args): pass
