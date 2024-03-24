from logging import Logger
from typing import Optional

from src.domain.constants import TRANSACTION_TIMER_NEEDED_ERROR
from src.domain.entities.product import Product
from src.domain.entities.vending_machine import VendingMachine


class RejectTransactionCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self) -> Optional[Product]:
        try:
            return self.vending_machine.reject_actual_transaction()
        except ValueError:
            self.logger.error(TRANSACTION_TIMER_NEEDED_ERROR)
            return None
