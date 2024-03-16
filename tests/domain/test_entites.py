import unittest
import datetime
from domain.entities.product import Product
from domain.constants import EXPIRATION_DATE_FORMAT_ERROR


class TestProduct(unittest.TestCase):
    def test_product_creation_with_invalid_expiration_date_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Product(name="Coke", price=2, expiration_date="not a date", code="1234")

        self.assertIn(EXPIRATION_DATE_FORMAT_ERROR, str(context.exception))

    def test_product_is_valid_with_future_expiration_date(self):
        future_date = datetime.date.today() + datetime.timedelta(days=10)
        product = Product(name="Coke", price=2, expiration_date=future_date, code="1234")
        self.assertTrue(product.is_valid())

    def test_product_is_not_valid_with_past_expiration_date(self):
        past_date = datetime.date.today() - datetime.timedelta(days=10)
        product = Product(name="Coke", price=2, expiration_date=past_date, code="1234")
        self.assertFalse(product.is_valid())


if __name__ == '__main__':
    unittest.main()
