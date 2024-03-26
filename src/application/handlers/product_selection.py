import logging

from src.application.commands.select_product import SelectProductCommand
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class ProductSelectionHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("ProductSelectionHandler")
        self.event_publisher = event_publisher
        self.select_product_command = SelectProductCommand(vending_machine, self.logger)

    def handle(self, payload):
        self.logger.info("Handling product selection")
        self.logger.info(f"Payload: {payload}")
        self.logger.info("Checking product by slot code")
        slot_code = payload
        try:
            price_product_selected = self.select_product_command.execute(slot_code)
            if not price_product_selected:
                self.event_publisher.publish("lcd/product", "No product selected.")
                return

            self.logger.info("Product selected successfully.")
            self.event_publisher.publish("lcd/product", str(price_product_selected))
            self.logger.info("Product price sent to LCD. 5 seconds to insert coins.")
        except ValueError:
            self.logger.error("Product not found")
            return
