from logging import Logger
from typing import Optional

from src.application.commands.check_vending_machine_status import (
    CheckVendingMachineCommand,
)
from src.domain.constants import PRODUCT_NOT_FOUND_ERROR, MachineStatus
from src.domain.entities.vending_machine import VendingMachine


class SelectProductCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger
        self.check_vending_machine_status = CheckVendingMachineCommand(
            vending_machine, logger
        )

    def execute(self, slot_code: str) -> Optional[float]:
        try:
            machine_status = self.check_vending_machine_status.execute()
            if machine_status != MachineStatus.AVAILABLE.value:
                return None
            return self.vending_machine.select_product(slot_code)
        except ValueError:
            self.logger.error(PRODUCT_NOT_FOUND_ERROR)
            return None
