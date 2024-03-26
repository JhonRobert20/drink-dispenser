from logging import Logger
from typing import Optional

from src.domain.constants import INVALID_COIN_ERROR, TransactionStatus
from src.domain.entities.vending_machine import VendingMachine


class DispenseProductCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self) -> Optional[TransactionStatus]:
        try:
            actual_slot_code = self.vending_machine.actual_slot_code
            if not actual_slot_code:
                self.logger.error("No product selected")
                return None
            return self.vending_machine.dispense_product(actual_slot_code)
        except ValueError:
            self.logger.error(INVALID_COIN_ERROR)
            return None
