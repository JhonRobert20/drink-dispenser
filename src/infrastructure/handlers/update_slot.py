import json
import logging

from src.infrastructure.config.db_connection import MongodbManager
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class UpdateSlotHandler:
    def __init__(self, mongo_db: MongodbManager, event_publisher: MqttEventPublisher):
        self.mongo_db = mongo_db
        self.logger = logging.getLogger("UpdateSlotHandler")
        self.event_publisher = event_publisher

    def handle(self, payload):
        self.logger.info("Handling update or create product slot")
        data = json.loads(payload)
        try:
            self.mongo_db.upsert_document(data, "product_slots", "code")
            self.logger.info(
                f"Product slot {data['code']} updated or created successfully."
            )
        except KeyError as e:
            self.logger.error(f"Missing data in payload: {e}")
            return
        except ValueError as e:
            self.logger.error(f"Invalid data format: {e}")
            return
