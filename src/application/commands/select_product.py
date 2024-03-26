from logging import Logger
from typing import Optional

from src.domain.constants import PRODUCT_NOT_FOUND_ERROR
from src.domain.entities.vending_machine import VendingMachine


class SelectProductCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self, slot_code: str) -> Optional[float]:
        try:
            return self.vending_machine.select_product(slot_code)
        except ValueError:
            self.logger.error(PRODUCT_NOT_FOUND_ERROR)
            return None
