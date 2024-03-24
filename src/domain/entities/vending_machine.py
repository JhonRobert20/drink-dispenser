from typing import Dict, List, Optional

from src.domain.constants import (
    COIN_ENTITY_REQUIRED_ERROR,
    INVALID_COIN_ERROR,
    SLOT_ENTITY_REQUIRED_ERROR,
    VENDING_MACHINE_ADD_PRODUCT_ERROR,
    TransactionStatus,
)
from src.domain.entities.product import Product
from src.domain.entities.product_slot import ProductSlot
from src.domain.entities.transaction import Transaction
from src.domain.utils import PeekableProductsQueue
from src.domain.value_objects.coin import Coin


class VendingMachine:
    def __init__(self, slots: Dict[str, ProductSlot], coins: List[Coin]):
        if not isinstance(slots, dict):
            raise ValueError(SLOT_ENTITY_REQUIRED_ERROR)
        if not isinstance(coins, list):
            raise ValueError(COIN_ENTITY_REQUIRED_ERROR)

        self.slots = slots
        self.coins = coins
        self.coins_actual_transaction = []

    def add_product_to_slot(self, product: Product, slot_code: str):
        slot: ProductSlot = self.get_slot_by_code(slot_code)
        if slot:
            if slot.products.get_without_consume().bar_code != product.bar_code:
                raise ValueError(VENDING_MACHINE_ADD_PRODUCT_ERROR)
            slot.products.put(product)
            return slot

        else:
            new_products_queue = PeekableProductsQueue([product])
            self.slots[slot_code] = ProductSlot(new_products_queue, slot_code)
            return self.slots[slot_code]

    def check_product_availability(self, slot_code: str):
        slot = self.get_slot_by_code(slot_code)
        if not slot:
            return False

        product = slot.products.get_without_consume()
        return product and product.is_valid()

    def check_can_expend(self, slot_code: str):
        if self.check_product_availability(slot_code):
            slot = self.get_slot_by_code(slot_code)
            coins_value = round(
                sum([coin.denomination for coin in self.coins_actual_transaction]), 2
            )
            if coins_value >= slot.products.get_without_consume().price:
                return True
        return False

    def dispense_product(self, slot_code: str):
        if self.check_can_expend(slot_code):
            slot = self.get_slot_by_code(slot_code)
            product_to_expend = slot.products.get_if_exists()
            paid_amount = sum(
                [coin.denomination for coin in self.coins_actual_transaction]
            )
            transaction = Transaction(
                product_to_expend, paid_amount, TransactionStatus.PENDING, self.coins
            )
            try:
                coins_index_to_return = transaction.validate_money()
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
        if not coin.is_valid():
            raise ValueError(INVALID_COIN_ERROR)

        self.coins.append(coin)
        self.coins_actual_transaction.append(coin)

    def get_slot_by_code(self, slot_code: str) -> Optional[ProductSlot]:
        if slot_code in self.slots:
            return self.slots[slot_code]
        return None

    def remove_slot(self, slot_code: str) -> Optional[ProductSlot]:
        if slot_code in self.slots:
            return self.slots.pop(slot_code)
        return None

    def check_stock_by_code(self, slot_code: str) -> int:
        if slot_code in self.slots:
            return self.slots[slot_code].products.qsize()
        return 0
