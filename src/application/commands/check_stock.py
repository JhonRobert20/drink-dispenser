from logging import Logger
from typing import Optional

from src.application.constants import CHECK_STOCK_ERROR
from src.domain.entities.product import Product
from src.domain.entities.vending_machine import VendingMachine


class CheckStockCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self) -> Optional[Product]:
        try:
            return self.vending_machine.list_product_stock()
        except ValueError:
            self.logger.error(CHECK_STOCK_ERROR)
            return None
