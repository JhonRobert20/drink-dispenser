import json
import logging

from src.application.commands.add_coin import AddCoinCommand
from src.domain.entities.vending_machine import VendingMachine
from src.domain.value_objects.coin import Coin
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class AddCoinHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("AddProductHandler")
        self.add_coin_command = AddCoinCommand(
            vending_machine=self.vending_machine, logger=self.logger
        )
        self.event_publisher = event_publisher

    def handle(self, payload):
        self.logger.info("Handling add coin")
        if self.vending_machine.actual_slot_code is None:
            self.logger.error("No product selected")
            self.event_publisher.publish("lcd/product", "No product selected.")
            return

        coin_data = json.loads(payload)
        self.logger.info(f"Coin data: {coin_data}")

        try:
            coin = Coin(
                denomination=coin_data["denomination"], currency=coin_data["currency"]
            )
            coin_inserted = self.add_coin_command.execute(coin)
            if coin_inserted:
                self.logger.info(f"Coin {coin.denomination} added successfully.")
                self.event_publisher.publish(
                    "lcd/product", f"Coin {coin.denomination} added successfully."
                )
            else:
                self.logger.info(f"Failed to add coin {coin.denomination}.")
                self.event_publisher.publish(
                    "lcd/product", f"Failed to add coin {coin.denomination}."
                )
        except KeyError as e:
            self.logger.error(f"Missing data in payload: {e}")
            self.event_publisher.publish("lcd/product", "Invalid coin data.")
            return
        except ValueError as e:
            self.logger.error(f"Invalid data format: {e}")
            self.event_publisher.publish("lcd/product", f"Invalid coin data: {e}.")
            return
