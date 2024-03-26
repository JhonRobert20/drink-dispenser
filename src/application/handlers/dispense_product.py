import json
import logging
from copy import copy

from src.application.commands.dispense_product import DispenseProductCommand
from src.domain.entities.product_slot import ProductSlot
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher
from src.infrastructure.persistence.models.product_slot import ProductSlotModel
from src.infrastructure.persistence.models.transaction import TransactionModel


class DispenseProductHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("DispenseProductHandler")
        self.event_publisher = event_publisher
        self.dispense_product_command = DispenseProductCommand(
            vending_machine, self.logger
        )

    def handle(self, payload):
        self.logger.info("Handling reject transaction")
        actual_slot_code = copy(self.vending_machine.actual_slot_code)
        if actual_slot_code is None:
            self.logger.error("No product selected")
            self.event_publisher.publish("lcd/product", "No product selected.")
            return
        self.logger.info("dispensing product")
        dispense_status, msg, populate_data = self.dispense_product_command.execute()
        self.event_publisher.publish("lcd/product", msg)
        self.event_publisher.publish(
            "lcd/product", f"Dispensed status: {dispense_status}"
        )
        if populate_data:
            self.logger.info("Populating data")
            slot_data: ProductSlot = populate_data["slot"]
            products_available = slot_data.products.qsize()
            if products_available == 0:
                self.event_publisher.publish(
                    "lcd/product",
                    f"No products available in slot code {actual_slot_code}.",
                )
                return
            transaction_model = TransactionModel(populate_data["transaction"])
            self.event_publisher.publish(
                "vending_machine/add_transaction",
                json.dumps(transaction_model.to_dict()),
            )
            slot_model = ProductSlotModel(populate_data["slot"])
            slot_model_json = json.dumps(slot_model.to_dict())
            self.event_publisher.publish("vending_machine/update_slot", slot_model_json)
