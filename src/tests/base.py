import datetime
import logging
import unittest

from src.domain.constants import MachineStatus
from src.domain.entities.product import Product
from src.domain.entities.vending_machine import ProductSlot, VendingMachine
from src.domain.utils import PeekableProductsQueue
from src.domain.value_objects.coin import Coin
from src.infrastructure.config.db_connection import MongodbManager
from src.infrastructure.mqtt.mqtt_client import start_and_configure_mqtt_client

logging.basicConfig(level=logging.DEBUG, filename="test.log", filemode="w")


class TestBase(unittest.TestCase):
    def setUp(self):
        self.product_coke = Product(
            name="Coke",
            price=1.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=5),
            bar_code="1111",
        )
        self.product_sprite = Product(
            name="Sprite",
            price=1.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=10),
            bar_code="2222",
        )
        self.will_expire_product = Product(
            name="Fanta",
            price=1.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=1),
            bar_code="3333",
        )
        self.to_expensive_product = Product(
            name="Fanta",
            price=10.00,
            expiration_date=datetime.date.today() + datetime.timedelta(days=1),
            bar_code="4444",
        )

        self.slot_coke = ProductSlot(
            products=PeekableProductsQueue([self.product_coke]), code="A1"
        )
        self.slot_to_expensive = ProductSlot(
            products=PeekableProductsQueue([self.to_expensive_product]), code="A2"
        )

        self.coin_05_eur = Coin(denomination=0.05, currency="EUR")
        self.coin_1_eur = Coin(denomination=1.00, currency="EUR")

        self.initial_coins = [self.coin_1_eur, self.coin_05_eur, self.coin_05_eur]
        self.len_initial_coins = len(self.initial_coins)
        self.initial_slot = {
            self.slot_coke.code: self.slot_coke,
            self.slot_to_expensive.code: self.slot_to_expensive,
        }

        self.initial_total_money = round(
            sum([coin.denomination for coin in self.initial_coins]), 2
        )

        self.vending_machine = VendingMachine(
            slots=self.initial_slot,
            coins=self.initial_coins,
        )
        self.vending_machine.slots = self.initial_slot
        self.vending_machine.coins = self.initial_coins
        self.mongo_db = MongodbManager(bd_name="test_drink_dispenser")
        self.logger = logging.getLogger("TestBase")

    def tearDown(self):
        self.mongo_db.drop_collection("product_slots")
        self.mongo_db.drop_collection("transactions")
        self.mongo_db.close_connection()
        self.vending_machine.actual_transaction = None
        self.vending_machine.timer = None
        self.vending_machine.machine_status = MachineStatus.AVAILABLE
        self.vending_machine.slots = {}
        self.vending_machine.coins_actual_transaction = []
        self.vending_machine.coins = []
        self.vending_machine.actual_product = None


class TestBaseMqtt(TestBase):
    def setUp(self):
        super().setUp()

        self.client = start_and_configure_mqtt_client(
            self.logger,
            self.mongo_db,
            vending_machine=self.vending_machine,
        )
        self.client.loop_start()

    def tearDown(self):
        super().tearDown()
        self.client.loop_stop()
        self.client.disconnect()
