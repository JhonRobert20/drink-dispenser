from src.domain.value_objects.coin import Coin


class CoinModel:
    def __init__(self, coin: Coin):
        self.denomination = coin.denomination
        self.amount = coin.currency

    def to_dict(self):
        return {
            "denomination": self.denomination,
            "amount": self.amount,
        }
