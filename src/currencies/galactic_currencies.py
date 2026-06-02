"""
Galactic Currency — Full 1,000 Token Registry
==============================================
Aggregates all 4 registry chunks into GALACTIC_CURRENCIES.
"""
from typing import Any, Dict, List
from .galactic_currencies_1 import GALACTIC_CURRENCIES_1
from .galactic_currencies_2 import GALACTIC_CURRENCIES_2
from .galactic_currencies_3 import GALACTIC_CURRENCIES_3
from .galactic_currencies_4 import GALACTIC_CURRENCIES_4

GALACTIC_CURRENCIES: List[Dict[str, Any]] = (
    GALACTIC_CURRENCIES_1 +
    GALACTIC_CURRENCIES_2 +
    GALACTIC_CURRENCIES_3 +
    GALACTIC_CURRENCIES_4
)

__all__ = ["GALACTIC_CURRENCIES"]
