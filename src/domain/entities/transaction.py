from typing import List

from src.domain.constants import (
    NOT_ENOUGH_COINS_ERROR,
    PRODUCT_ENTITY_REQUIRED_ERROR,
    TRANSACTION_FLOAT_TYPE_ERROR,
    TRANSACTION_STATUS_TYPE_ERROR,
    TransactionStatus,
)
from src.domain.entities.product import Product
from src.domain.value_objects.coin import Coin


class Transaction:
    def __init__(
        self,
        product: Product,
        paid_amount: float,
        status: TransactionStatus,
        coins_in_machine: List[Coin],
    ):
        if not isinstance(product, Product):
            raise ValueError(PRODUCT_ENTITY_REQUIRED_ERROR)

        if not isinstance(status, TransactionStatus):
            raise ValueError(TRANSACTION_STATUS_TYPE_ERROR)

        if not isinstance(paid_amount, float) and paid_amount != 0:
            raise ValueError(TRANSACTION_FLOAT_TYPE_ERROR)

        self.product = product
        self.paid_amount = paid_amount
        self.change_amount = round(paid_amount - product.price, 2)
        self.status = status
        self.coins_in_machine = coins_in_machine

    def __str__(self):
        return f"Transaction: {self.product} with status: {self.status}"

    def mark_as_completed(self):
        self.status = TransactionStatus.COMPLETED
        return self.status

    def mark_as_pending(self):
        self.status = TransactionStatus.PENDING
        return self.status

    def mark_as_error(self):
        self.status = TransactionStatus.ERROR
        return self.status

    def mark_as_cancelled(self):
        self.status = TransactionStatus.CANCELLED
        return self.status

    def mark_as_refunded(self):
        self.status = TransactionStatus.REFUNDED
        return self.status

    def validate_money(self) -> List[int]:
        if self.change_amount < 0:
            raise ValueError(NOT_ENOUGH_COINS_ERROR)

        coins_in_machine = self.coins_in_machine
        change_amount = self.change_amount
        sorted_coins = sorted(
            ((coin.denomination, i) for i, coin in enumerate(coins_in_machine)),
            reverse=True,
        )

        coins_to_return = []
        total_change_given = 0.0

        for denomination, index in sorted_coins:
            maybe_total = round(total_change_given + denomination, 2)
            if maybe_total > change_amount:
                continue

            total_change_given = maybe_total
            coins_to_return.append(index)

            if total_change_given == change_amount:
                return coins_to_return

        raise ValueError(NOT_ENOUGH_COINS_ERROR)
