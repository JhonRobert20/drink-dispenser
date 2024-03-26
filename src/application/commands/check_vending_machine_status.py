from logging import Logger

from src.domain.entities.vending_machine import VendingMachine


class CheckVendingMachineCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self) -> str:
        self.logger.info("Checking vending machine status")
        machine_status = self.vending_machine.get_machine_status()
        self.logger.info(f"Vending machine status: {machine_status}")
        return machine_status
