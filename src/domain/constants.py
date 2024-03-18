from enum import Enum

PRODUCT_EXPIRATION_FORMAT_ERROR = "expiration date must be a datetime.date instance"
PRODUCT_ENTITY_REQUIRED_ERROR = "product must be a Product instance"
TRANSACTION_STATUS_TYPE_ERROR = "status must be a TransactionStatus instance"
TRANSACTION_FLOAT_TYPE_ERROR = "paid amount and change given must be float instances"
VENDING_MACHINE_ADD_PRODUCT_ERROR = (
    "The slot is already occupied with a different product"
)
NOT_ENOUGH_COINS_ERROR = "Not enough coins to give change, returning paid amount."
INVALID_COIN_ERROR = "Invalid coin denomination or currency"


class TransactionStatus(Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    ERROR = "error"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


COIN_VALID_DENOMINATIONS = [0.05, 0.10, 0.20, 0.50, 1.00, 2.00]
COIN_VALID_CURRENCY = ["EUR"]
