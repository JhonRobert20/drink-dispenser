import logging

from infrastructure.config.db_connection import MongodbManager
from infrastructure.mqtt.mqtt_client import start_and_configure_mqtt_client
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.persistence.repositori_impl.product_slot import (
    ProductSlotRepositoryImpl,
)
from src.infrastructure.persistence.repositori_impl.transaction import (
    TransactionRepositoryImpl,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    product_slot_impl = ProductSlotRepositoryImpl(MongodbManager("drink_dispenser"))
    transaction_impl = TransactionRepositoryImpl(MongodbManager("drink_dispenser"))

    product_slots = product_slot_impl.list_product_slots()
    coins = transaction_impl.get_coins_from_last_transaction()

    vending_machine = VendingMachine(product_slots, coins)

    start_and_configure_mqtt_client(
        logger=logger,
        vending_machine=vending_machine,
    )


main()
