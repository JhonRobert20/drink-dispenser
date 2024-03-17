from typing import List

from src.domain.constants import VENDING_MACHINE_ADD_PRODUCT_ERROR
from src.domain.entities.product import Product
from src.domain.utils import PeekableProductsQueue


class ProductSlot:
    def __init__(self, products: PeekableProductsQueue, code: str):
        self.products = products
        self.code = code


class VendingMachine:
    def __init__(self, slots: List[ProductSlot]):
        self.slots = slots

    def add_product_to_slot(self, product: Product, slot_code: str):
        slot = self.get_slot_by_code(slot_code)
        if slot:
            if slot.products.get_without_consume().bar_code != product.bar_code:
                raise ValueError(VENDING_MACHINE_ADD_PRODUCT_ERROR)
            slot.products.put(product)

        else:
            new_products_queue = PeekableProductsQueue([product])
            self.slots.append(ProductSlot(new_products_queue, slot_code))

    def check_if_can_expend(self, slot_index: int):
        product = self.slots[slot_index].products.get_if_exists()
        if product:
            return product.is_valid()
        return False

    def consume_product_item(self, slot_index: int):
        return self.slots[slot_index].products.get_if_exists()

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
