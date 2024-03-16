from enum import Enum

EXPIRATION_DATE_FORMAT_ERROR = "expiration date must be a datetime.date instance"
PRODUCT_ENTITY_REQUIRED_ERROR = "product must be a Product instance"
TRANSACTION_STATUS_TYPE_ERROR = "status must be a TransactionStatus instance"
TRANSACTION_FLOAT_TYPE_ERROR = "paid amount and change given must be float instances"

class TransactionStatus(Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    ERROR = "error"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"