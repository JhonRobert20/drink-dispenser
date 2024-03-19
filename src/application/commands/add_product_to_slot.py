from logging import Logger
from typing import Optional

from src.application.constants import MISMATCHED_PRODUCT_ERROR
from src.domain.entities.product import Product
from src.domain.entities.product_slot import ProductSlot
from src.domain.entities.vending_machine import VendingMachine


class AddProductToSlotCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self, product: Product, slot_code: str) -> Optional[ProductSlot]:
        try:
            return self.vending_machine.add_product_to_slot(product, slot_code)
        except ValueError:
            self.logger.error(MISMATCHED_PRODUCT_ERROR)
            return None
