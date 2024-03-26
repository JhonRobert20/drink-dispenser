import time
import unittest

from src.domain.constants import MachineStatus
from src.infrastructure.persistence.repositori_impl.product_slot import (
    ProductSlotRepositoryImpl,
)
from src.tests.base import TestBaseMqtt


class MqttIntegrationTest(TestBaseMqtt):
    def test_add_product_via_mqtt(self):
        product_slot_repo = ProductSlotRepositoryImpl(self.mongo_db)
        stock_count = self.vending_machine.check_stock_by_code("B4")
        product_slots = product_slot_repo.list_product_slots()

        self.assertEqual(stock_count, 0)
        self.assertEqual(len(product_slots), 0)

        self.client.publish(
            "vending_machine/add",
            '{"product":'
            '{"name": "Coke", "price": 2,'
            ' "expiration_date": "2023-12-31", "bar_code": "1234"},'
            '"slot_code": "B4"}',
        )

        time.sleep(1)
        product_slots = product_slot_repo.list_product_slots()
        stock_count = self.vending_machine.check_stock_by_code("B4")
        self.assertEqual(stock_count, 1)
        self.assertEqual(len(product_slots), 1)

    def test_consult_stock(self):
        self.client.publish("vending_machine/consult_stock", "")

    def test_check_machine_status(self):
        self.client.publish("vending_machine/consult_status", "")

    def test_select_product(self):
        self.client.publish(
            "vending_machine/add",
            '{"product":'
            '{"name": "Coke", "price": 2,'
            ' "expiration_date": "2023-12-31", "bar_code": "1234"},'
            '"slot_code": "B4"}',
        )

        time.sleep(1)
        self.client.publish("vending_machine/selections", "B4")
        time.sleep(1)
        assert self.vending_machine.get_machine_status() == MachineStatus.BUSY.value
        time.sleep(4.5)
        assert (
            self.vending_machine.get_machine_status() == MachineStatus.AVAILABLE.value
        )

    def test_reject_transaction_no_product(self):
        self.vending_machine.actual_product = None
        self.client.publish("vending_machine/reject_transaction", "")
        assert (
            self.vending_machine.get_machine_status() == MachineStatus.AVAILABLE.value
        )

    def test_reject_transaction(self):
        self.client.publish(
            "vending_machine/add",
            '{"product":'
            '{"name": "Coke", "price": 2,'
            ' "expiration_date": "2023-12-31", "bar_code": "1234"},'
            '"slot_code": "B4"}',
        )

        time.sleep(1)
        self.client.publish("vending_machine/selections", "B4")
        time.sleep(1)
        assert self.vending_machine.get_machine_status() == MachineStatus.BUSY.value
        time.sleep(4.5)
        assert (
            self.vending_machine.get_machine_status() == MachineStatus.AVAILABLE.value
        )
        self.client.publish("vending_machine/reject_transaction", "")
        assert (
            self.vending_machine.get_machine_status() == MachineStatus.AVAILABLE.value
        )


if __name__ == "__main__":
    unittest.main()
