from logging import Logger
from typing import Optional

from src.domain.constants import INVALID_COIN_ERROR, TransactionStatus
from src.domain.entities.vending_machine import VendingMachine


class DispenseProductCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self, slot_code: str) -> Optional[TransactionStatus]:
        try:
            return self.vending_machine.dispense_product(slot_code)
        except ValueError:
            self.logger.error(INVALID_COIN_ERROR)
            return None
