import json
import logging

from src.application.commands.check_stock import CheckStockCommand
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class ConsultStockHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("ConsultStockHandler")
        self.event_publisher = event_publisher
        self.check_stock_command = CheckStockCommand(vending_machine, self.logger)

    def handle(self, payload):
        self.logger.info("Handling consult stock")
        self.logger.info(f"Payload: {payload}")
        product_slot_repo = self.check_stock_command.execute()
        self.logger.info("Stock checked successfully.")
        self.event_publisher.publish("lcd/stock", json.dumps(product_slot_repo))
