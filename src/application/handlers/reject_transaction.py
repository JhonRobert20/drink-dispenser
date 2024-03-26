import logging

from src.application.commands.reject_transaction import RejectTransactionCommand
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class RejectTransactionHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("ProductSelectionHandler")
        self.event_publisher = event_publisher
        self.reject_transaction_product = RejectTransactionCommand(
            vending_machine, self.logger
        )

    def handle(self, payload):
        self.logger.info("Handling reject transaction")
        if self.vending_machine.actual_slot_code is None:
            self.logger.error("No product selected")
            self.event_publisher.publish("lcd/product", "No product selected.")
            return
        self.logger.info("Rejecting transaction")
        self.reject_transaction_product.execute()
        self.event_publisher.publish("lcd/product", "Rejected successfully.")
