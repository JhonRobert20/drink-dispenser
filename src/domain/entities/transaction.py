from src.domain.constants import (
    PRODUCT_ENTITY_REQUIRED_ERROR,
    TRANSACTION_FLOAT_TYPE_ERROR,
    TRANSACTION_STATUS_TYPE_ERROR,
    TransactionStatus,
)
from src.domain.entities.product import Product


class Transaction:
    def __init__(
        self,
        product: Product,
        paid_amount: float,
        change_given: float,
        status: TransactionStatus,
    ):
        if not isinstance(product, Product):
            raise ValueError(PRODUCT_ENTITY_REQUIRED_ERROR)

        if not isinstance(status, TransactionStatus):
            raise ValueError(TRANSACTION_STATUS_TYPE_ERROR)

        if not isinstance(paid_amount, float) or not isinstance(change_given, float):
            raise ValueError(TRANSACTION_FLOAT_TYPE_ERROR)

        self.product = product
        self.paid_amount = paid_amount
        self.change_given = change_given
        self.status = status

    def __str__(self):
        return f"Transaction: {self.product} with status: {self.status}"

    def mark_as_completed(self):
        self.status = TransactionStatus.COMPLETED

    def mark_as_pending(self):
        self.status = TransactionStatus.PENDING

    def mark_as_error(self):
        self.status = TransactionStatus.ERROR

    def mark_as_cancelled(self):
        self.status = TransactionStatus.CANCELLED

    def mark_as_refunded(self):
        self.status = TransactionStatus.REFUNDED
