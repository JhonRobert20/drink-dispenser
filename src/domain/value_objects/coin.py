from dataclasses import dataclass

from src.domain.constants import COIN_VALID_CURRENCY, COIN_VALID_DENOMINATIONS


@dataclass(frozen=True)
class Coin:
    denomination: float
    currency: str

    def is_valid(self):
        return (
            self.denomination in COIN_VALID_DENOMINATIONS
            and self.currency in COIN_VALID_CURRENCY
        )
