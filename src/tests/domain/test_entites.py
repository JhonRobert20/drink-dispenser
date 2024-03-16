import datetime
import unittest

from src.domain.constants import (
    PRODUCT_ENTITY_REQUIRED_ERROR,
    PRODUCT_EXPIRATION_FORMAT_ERROR,
    TRANSACTION_FLOAT_TYPE_ERROR,
    TRANSACTION_STATUS_TYPE_ERROR,
    TransactionStatus,
)
from src.domain.entities.product import Product
from src.domain.entities.transaction import Transaction


class TestProduct(unittest.TestCase):
    def test_product_creation_with_invalid_expiration_date_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Product(name="Coke", price=2, expiration_date="not a date", code="1234")

        self.assertIn(PRODUCT_EXPIRATION_FORMAT_ERROR, str(context.exception))

    def test_product_is_valid_with_future_expiration_date(self):
        future_date = datetime.date.today() + datetime.timedelta(days=10)
        product = Product(
            name="Coke", price=2, expiration_date=future_date, code="1234"
        )
        self.assertTrue(product.is_valid())

    def test_product_is_not_valid_with_past_expiration_date(self):
        past_date = datetime.date.today() - datetime.timedelta(days=10)
        product = Product(name="Coke", price=2, expiration_date=past_date, code="1234")
        self.assertFalse(product.is_valid())


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.product = Product(
            name="Coke",
            price=2,
            expiration_date=datetime.date.today() + datetime.timedelta(days=10),
            code="1234",
        )
        self.invalid_product = "not a product instance"

    def test_transaction_creation_invalid_product(self):
        with self.assertRaises(ValueError) as context:
            Transaction(
                product=self.invalid_product,
                paid_amount=2,
                change_given=0,
                status=TransactionStatus.PENDING,
            )
        self.assertIn(PRODUCT_ENTITY_REQUIRED_ERROR, str(context.exception))

    def test_transaction_creation_invalid_status(self):
        with self.assertRaises(ValueError) as context:
            Transaction(
                product=self.product,
                paid_amount=2.0,
                change_given=0.0,
                status="invalid status",
            )
        self.assertIn(TRANSACTION_STATUS_TYPE_ERROR, str(context.exception))

    def test_transaction_creation_invalid_floats(self):
        with self.assertRaises(ValueError) as context:
            Transaction(
                product=self.product,
                paid_amount=2,
                change_given=2,
                status=TransactionStatus.PENDING,
            )
        self.assertIn(TRANSACTION_FLOAT_TYPE_ERROR, str(context.exception))

    def test_transaction_creation(self):
        transaction = Transaction(
            product=self.product,
            paid_amount=2.0,
            change_given=0.0,
            status=TransactionStatus.PENDING,
        )
        self.assertEqual(transaction.product, self.product)
        self.assertEqual(transaction.paid_amount, 2)
        self.assertEqual(transaction.change_given, 0)
        self.assertEqual(transaction.status, TransactionStatus.PENDING)
        transaction.mark_as_completed()
        self.assertEqual(transaction.status, TransactionStatus.COMPLETED)


if __name__ == "__main__":
    unittest.main()
