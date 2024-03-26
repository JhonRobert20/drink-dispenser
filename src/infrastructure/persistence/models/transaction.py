from datetime import datetime

from src.domain.entities.transaction import Transaction
from src.infrastructure.persistence.models.coin import CoinModel
from src.infrastructure.persistence.models.product import ProductModel


class TransactionModel:
    def __init__(self, transaction: Transaction):
        self.product = transaction.product
        self.paid_amount = transaction.paid_amount
        self.change_amount = transaction.change_amount
        self.status = transaction.status
        self.coins_in_machine = [
            CoinModel(coin) for coin in transaction.coins_in_machine
        ]

    def to_dict(self):
        return {
            "product": ProductModel(self.product).to_dict(),
            "paid_amount": self.paid_amount,
            "change_amount": self.change_amount,
            "status": self.status,
            "date": datetime.now().isoformat(),
            "coins": [coin.to_dict() for coin in self.coins_in_machine],
        }
