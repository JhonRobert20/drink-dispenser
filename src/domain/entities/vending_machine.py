from typing import List

from src.domain.constants import (
    INVALID_COIN_ERROR,
    VENDING_MACHINE_ADD_PRODUCT_ERROR,
    TransactionStatus,
)
from src.domain.entities.product import Product
from src.domain.entities.transaction import Transaction
from src.domain.utils import PeekableProductsQueue
from src.domain.value_objects.coin import Coin


class ProductSlot:
    def __init__(self, products: PeekableProductsQueue, code: str):
        self.products = products
        self.code = code


class VendingMachine:
    def __init__(self, slots: List[ProductSlot], coins: List[Coin]):
        self.slots = slots
        self.coins = coins
        self.coins_actual_transaction = []

    def add_product_to_slot(self, product: Product, slot_code: str):
        slot = self.get_slot_by_code(slot_code)
        if slot:
            if slot.products.get_without_consume().bar_code != product.bar_code:
                raise ValueError(VENDING_MACHINE_ADD_PRODUCT_ERROR)
            slot.products.put(product)

        else:
            new_products_queue = PeekableProductsQueue([product])
            self.slots.append(ProductSlot(new_products_queue, slot_code))

    def product_is_valid(self, slot_index: int):
        product = self.slots[slot_index].products.get_without_consume()
        if product:
            return product.is_valid()
        return False

    def check_can_expend(self, slot_index: int):
        if self.product_is_valid(slot_index):
            coins_value = round(
                sum([coin.denomination for coin in self.coins_actual_transaction]), 2
            )
            if (
                coins_value
                >= self.slots[slot_index].products.get_without_consume().price
            ):
                return True
        return False

    def consume_product_item(self, slot_index: int):
        if self.check_can_expend(slot_index):
            product_to_expend = self.slots[slot_index].products.get_if_exists()
            paid_amount = sum(
                [coin.denomination for coin in self.coins_actual_transaction]
            )
            transaction = Transaction(
                product_to_expend, paid_amount, TransactionStatus.PENDING, self.coins
            )
            try:
                coins_index_to_return = transaction.calculate_change_to_give()
                self.__remove_coins_from_machine(coins_index_to_return)
                transaction.mark_as_completed()
            except ValueError:
                transaction.mark_as_error()
                index_to_remove = [i for i in range(len(self.coins_actual_transaction))]
                self.__remove_coins_from_machine(index_to_remove)
        else:
            index_to_remove = [i for i in range(len(self.coins_actual_transaction))]
            self.__remove_coins_from_machine(index_to_remove)

    def __remove_coins_from_machine(self, coins_index_to_return: List[int]):
        ordered_coins_index = sorted(coins_index_to_return, reverse=True)
        for index in ordered_coins_index:
            self.coins.pop(index)
        self.coins_actual_transaction = []

    def add_coin_to_transaction(self, coin: Coin):
        self.coins.append(coin)
        self.coins_actual_transaction.append(coin)
        if not coin.is_valid():
            self.coins_actual_transaction.pop()
            self.coins.pop()
            raise ValueError(INVALID_COIN_ERROR)

    def get_existing_slot_index(self, slot_code: str):
        for slot in self.slots:
            if slot.code == slot_code:
                return self.slots.index(slot)
        return None

    def get_slot_by_code(self, slot_code: str):
        for slot in self.slots:
            if slot.code == slot_code:
                return slot
        return None

    def remove_slot(self, slot_code: str):
        for slot in self.slots:
            if slot.code == slot_code:
                self.slots.remove(slot)

    def check_stock_by_code(self, slot_code: str):
        for slot in self.slots:
            if slot.code == slot_code:
                return slot.products.qsize()
        return 0

    def check_stock_by_index(self, index: int):
        return self.slots[index].products.qsize()

    def check_all_stock(self):
        return {
            slot.code: (slot.products.qsize(), slot.products.get_name_without_consume())
            for slot in self.slots
        }
