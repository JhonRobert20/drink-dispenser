from typing import Optional

from src.application.commands.add_coin import AddCoinCommand
from src.application.commands.dispense_product import DispenseProductCommand
from src.application.commands.reject_transaction import RejectTransactionCommand
from src.application.commands.select_product import SelectProductCommand
from src.domain.constants import TransactionStatus
from src.domain.entities.vending_machine import VendingMachine


class DispensingService:
    def __init__(self, vending_machine: VendingMachine, logger):
        self.vending_machine = vending_machine
        self.logger = logger
        self.select_product_command = SelectProductCommand(vending_machine, logger)
        self.selected_slot_code: Optional[str] = None
        self.add_coin_command = AddCoinCommand(vending_machine, logger)
        self.dispense_product_command = DispenseProductCommand(vending_machine, logger)
        self.reject_transaction_command = RejectTransactionCommand(
            vending_machine, logger
        )

    def start_transaction(self, slot_code: str) -> bool:
        self.logger.info("Dispensing service initialized")
        transaction = self.select_product_command.execute(slot_code)
        self.selected_slot_code = slot_code
        return transaction is not None

    def add_coin(self, coin_denomination: float) -> bool:
        result = self.add_coin_command.execute(coin_denomination)
        return result is not None

    def finalize_transaction(self) -> Optional[TransactionStatus]:
        self.logger.info("Finalizing transaction")
        status = self.dispense_product_command.execute(self.selected_slot_code)
        return status

    def cancel_transaction(self) -> bool:
        status = self.reject_transaction_command.execute()
        self.selected_slot_code = None
        return status is not None
