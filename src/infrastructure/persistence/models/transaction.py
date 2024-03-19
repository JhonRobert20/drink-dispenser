from src.domain.entities.transaction import Transaction
from src.infrastructure.persistence.models.coin import CoinModel


class TransactionModel:
    def __init__(self, transaction: Transaction):
        self.product = transaction.product
        self.paid_amount = transaction.paid_amount
        self.change_amount = transaction.change_amount
        self.status = transaction.status
        self.coins_in_machine = [
            CoinModel(coin) for coin in transaction.coins_in_machine
        ]
