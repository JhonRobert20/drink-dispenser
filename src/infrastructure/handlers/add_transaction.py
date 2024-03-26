import json
import logging

from src.infrastructure.config.db_connection import MongodbManager
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class AddTransactionHandler:
    def __init__(self, mongo_db: MongodbManager, event_publisher: MqttEventPublisher):
        self.mongo_db = mongo_db
        self.logger = logging.getLogger("AddTransactionHandler")
        self.event_publisher = event_publisher

    def handle(self, payload):
        self.logger.info("Handling add transaction in mongo db")
        data = json.loads(payload)
        try:
            document_id = self.mongo_db.insert_document("transactions", data)
            self.logger.info(
                f"Transaction created successfully with document code {document_id}."
            )
        except KeyError as e:
            self.logger.error(f"Missing data in payload: {e}")
            return
        except ValueError as e:
            self.logger.error(f"Invalid data format: {e}")
            return
