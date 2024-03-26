import datetime
import json
import logging
from typing import Optional

from src.application.commands.add_product_to_slot import AddProductToSlotCommand
from src.domain.entities.product import Product
from src.domain.entities.product_slot import ProductSlot
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher
from src.infrastructure.persistence.models.product_slot import ProductSlotModel


class AddProductHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("AddProductHandler")
        self.add_product_command = AddProductToSlotCommand(
            vending_machine=self.vending_machine, logger=self.logger
        )
        self.event_publisher = event_publisher

    def set_event_publisher(self, event_publisher):
        self.event_publisher = event_publisher

    def handle(self, payload):
        self.logger.info("Handling add product")
        data = json.loads(payload)
        try:
            product_data = data["product"]
            product = Product(
                name=product_data["name"],
                price=product_data["price"],
                expiration_date=datetime.datetime.strptime(
                    product_data["expiration_date"], "%Y-%m-%d"
                ).date(),
                bar_code=product_data["bar_code"],
            )
            slot_code = data["slot_code"]
        except KeyError as e:
            self.logger.error(f"Missing data in payload: {e}")
            return
        except ValueError as e:
            self.logger.error(f"Invalid data format: {e}")
            return

        product_slot: Optional[ProductSlot] = self.add_product_command.execute(
            product, slot_code
        )

        if product_slot:
            self.logger.info(
                f"Product {product.name} added to slot {slot_code} successfully."
            )
            slot_model = ProductSlotModel(product_slot)
            slot_model_json = json.dumps(slot_model.to_dict())
            self.event_publisher.publish("vending_machine/update_slot", slot_model_json)
        else:
            self.logger.info(
                f"Failed to add product {product.name} to slot {slot_code}."
            )
