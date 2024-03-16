from dataclasses import dataclass
from domain.constants import COIN_VALID_DENOMINATIONS, COIN_VALID_CURRENCY
@dataclass(frozen=True)
class Coin:
    denomination: float
    currency: str

    def is_valid(self):
        return self.denomination in COIN_VALID_DENOMINATIONS and self.currency in COIN_VALID_CURRENCY