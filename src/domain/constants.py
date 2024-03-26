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
SLOT_ENTITY_REQUIRED_ERROR = "Slots must be a dictionary"
COIN_ENTITY_REQUIRED_ERROR = "Coins must be a list of Coin instances"
PRODUCT_NOT_FOUND_ERROR = "Product not found"
TRANSACTION_TIMER_NEEDED_ERROR = (
    "Transaction and timer needed, use the application layer"
)

DISPENSE_PRODUCT_SUCCESS_MSG = "Product dispensed successfully"
DISPENSE_PRODUCT_ERROR_MSG = "Error dispensing product, product not available"


class TransactionStatus(Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    ERROR = "error"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class MachineStatus(Enum):
    BUSY = "busy"
    OUT_OF_ORDER = "out_of_order"
    AVAILABLE = "available"


COIN_VALID_DENOMINATIONS = [0.05, 0.10, 0.20, 0.50, 1.00, 2.00]
COIN_VALID_CURRENCY = ["EUR"]
