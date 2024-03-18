import datetime
import unittest

from src.domain.constants import (
    INVALID_COIN_ERROR,
    PRODUCT_ENTITY_REQUIRED_ERROR,
    PRODUCT_EXPIRATION_FORMAT_ERROR,
    TRANSACTION_FLOAT_TYPE_ERROR,
    TRANSACTION_STATUS_TYPE_ERROR,
    VENDING_MACHINE_ADD_PRODUCT_ERROR,
    TransactionStatus,
)
from src.domain.entities.product import Product
from src.domain.entities.transaction import Transaction
from src.domain.entities.vending_machine import ProductSlot, VendingMachine
from src.domain.utils import PeekableProductsQueue
from src.domain.value_objects.coin import Coin


class TestProduct(unittest.TestCase):
    def test_product_creation_with_invalid_expiration_date_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Product(name="Coke", price=2, expiration_date="not a date", bar_code="1234")

        self.assertIn(PRODUCT_EXPIRATION_FORMAT_ERROR, str(context.exception))

    def test_product_is_valid_with_future_expiration_date(self):
        future_date = datetime.date.today() + datetime.timedelta(days=10)
        product = Product(
            name="Coke", price=2, expiration_date=future_date, bar_code="1234"
        )
        self.assertTrue(product.is_valid())

    def test_product_is_not_valid_with_past_expiration_date(self):
        past_date = datetime.date.today() - datetime.timedelta(days=10)
        product = Product(
            name="Coke", price=2, expiration_date=past_date, bar_code="1234"
        )
        self.assertFalse(product.is_valid())


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.product = Product(
            name="Coke",
            price=2,
            expiration_date=datetime.date.today() + datetime.timedelta(days=10),
            bar_code="1234",
        )
        self.invalid_product = "not a product instance"

    def test_transaction_creation_invalid_product(self):
        with self.assertRaises(ValueError) as context:
            Transaction(
                product=self.invalid_product,
                paid_amount=2,
                status=TransactionStatus.PENDING,
                coins_in_machine=[],
            )
        self.assertIn(PRODUCT_ENTITY_REQUIRED_ERROR, str(context.exception))

    def test_transaction_creation_invalid_status(self):
        with self.assertRaises(ValueError) as context:
            Transaction(
                product=self.product,
                paid_amount=2.0,
                status="invalid status",
                coins_in_machine=[],
            )
        self.assertIn(TRANSACTION_STATUS_TYPE_ERROR, str(context.exception))

    def test_transaction_creation_invalid_floats(self):
        with self.assertRaises(ValueError) as context:
            Transaction(
                product=self.product,
                paid_amount=2,
                status=TransactionStatus.PENDING,
                coins_in_machine=[],
            )
        self.assertIn(TRANSACTION_FLOAT_TYPE_ERROR, str(context.exception))

    def test_transaction_creation(self):
        transaction = Transaction(
            product=self.product,
            paid_amount=2.0,
            status=TransactionStatus.PENDING,
            coins_in_machine=[],
        )
        self.assertEqual(transaction.product, self.product)
        self.assertEqual(transaction.paid_amount, 2)
        self.assertEqual(transaction.status, TransactionStatus.PENDING)
        transaction.mark_as_completed()
        self.assertEqual(transaction.status, TransactionStatus.COMPLETED)


class TestVendingMachine(unittest.TestCase):
    def setUp(self):
        self.product_coke = Product(
            name="Coke",
            price=1.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=5),
            bar_code="1111",
        )
        self.product_sprite = Product(
            name="Sprite",
            price=1.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=10),
            bar_code="2222",
        )
        self.will_expire_product = Product(
            name="Fanta",
            price=1.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=1),
            bar_code="3333",
        )
        self.to_expensive_product = Product(
            name="Fanta",
            price=10.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=1),
            bar_code="4444",
        )

        self.slot_coke = ProductSlot(
            products=PeekableProductsQueue([self.product_coke]), code="A1"
        )
        self.slot_to_expensive = ProductSlot(
            products=PeekableProductsQueue([self.to_expensive_product]), code="A2"
        )

        self.coin_05_eur = Coin(denomination=0.05, currency="EUR")
        self.coin_1_eur = Coin(denomination=1.00, currency="EUR")

        self.initial_coins = [self.coin_1_eur, self.coin_05_eur, self.coin_05_eur]
        self.initial_slot = [self.slot_coke, self.slot_to_expensive]

        self.initial_total_money = round(
            sum([coin.denomination for coin in self.initial_coins]), 2
        )

        self.vending_machine = VendingMachine(
            slots=self.initial_slot,
            coins=self.initial_coins,
        )

    def test_add_different_product_to_existing_slot(self):
        with self.assertRaises(ValueError) as context:
            self.vending_machine.add_product_to_slot(self.product_sprite, "A1")
        self.assertIn(VENDING_MACHINE_ADD_PRODUCT_ERROR, str(context.exception))

    def test_add_product_to_new_slot(self):
        self.vending_machine.add_product_to_slot(self.product_sprite, "B2")
        slot = self.vending_machine.get_slot_by_code("B2")
        self.assertIsNotNone(slot)
        self.assertEqual(slot.products.qsize(), 1)

    def test_transaction_with_change(self):
        self.assertEqual(len(self.vending_machine.coins_actual_transaction), 0)
        slot = self.vending_machine.get_slot_by_code("A1")

        self.vending_machine.add_coin_to_transaction(
            Coin(denomination=1.00, currency="EUR")
        )
        self.vending_machine.add_coin_to_transaction(
            Coin(denomination=0.20, currency="EUR")
        )
        total_money = round(
            sum([coin.denomination for coin in self.vending_machine.coins]), 2
        )
        assert total_money == 2.30
        total_money_transaction = round(
            sum(
                [
                    coin.denomination
                    for coin in self.vending_machine.coins_actual_transaction
                ]
            ),
            2,
        )
        assert total_money_transaction == 1.20
        product_price = slot.products.get_without_consume().price
        expected_change = round(total_money_transaction - product_price, 2)
        assert expected_change == 0.20

        money_after_transaction = round(total_money - expected_change, 2)
        assert money_after_transaction == 2.10

        self.assertEqual(slot.products.qsize(), 1)
        self.assertEqual(len(self.vending_machine.coins_actual_transaction), 2)
        self.vending_machine.consume_product_item(0)
        total_money_after_transaction = round(
            sum([coin.denomination for coin in self.vending_machine.coins]), 2
        )
        assert total_money_after_transaction == money_after_transaction

        self.assertEqual(slot.products.qsize(), 0)

        self.assertEqual(len(self.vending_machine.coins_actual_transaction), 0)
        self.assertEqual(len(self.vending_machine.coins), 4)

    def test_transaction_without_change(self):
        self.vending_machine.consume_product_item(1)
        slot = self.vending_machine.get_slot_by_code(self.slot_to_expensive.code)
        self.assertEqual(slot.products.qsize(), 1)
        self.assertEqual(len(self.vending_machine.coins_actual_transaction), 0)
        self.assertEqual(len(self.vending_machine.coins), 3)

    def test_check_stock_by_code(self):
        stock_count = self.vending_machine.check_stock_by_code("A1")
        self.assertEqual(stock_count, 1)

    def test_check_all_stock(self):
        all_stock = self.vending_machine.check_all_stock()
        self.assertIn("A1", all_stock)
        self.assertEqual(all_stock["A1"][0], self.initial_slot[0].products.qsize())
        self.assertEqual(all_stock["A1"][1], self.product_coke.name)

    def test_expired_product_is_not_valid(self):
        self.will_expire_product.expiration_date = (
            datetime.date.today() - datetime.timedelta(days=1)
        )
        slot_queue = PeekableProductsQueue([self.will_expire_product])
        slot = ProductSlot(products=slot_queue, code="A3")
        self.vending_machine.slots.append(slot)
        self.assertFalse(self.vending_machine.product_is_valid(2))

    def test_add_invalid_coin_to_transaction(self):
        coin = Coin(denomination=0.001, currency="EUR")
        with self.assertRaises(ValueError) as context:
            self.vending_machine.add_coin_to_transaction(coin)
        self.assertIn(INVALID_COIN_ERROR, str(context.exception))
        self.assertEqual(len(self.vending_machine.coins_actual_transaction), 0)
        self.assertEqual(len(self.vending_machine.coins), len(self.initial_coins))
