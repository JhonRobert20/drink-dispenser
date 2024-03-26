import time
import unittest

from src.tests.base import TestBaseMqtt


class MqttIntegrationTest(TestBaseMqtt):
    def test_add_product_via_mqtt(self):
        self.client.publish(
            "vending_machine/add",
            '{"product":'
            '{"name": "Coke", "price": 2,'
            ' "expiration_date": "2023-12-31", "bar_code": "1234"},'
            '"slot_code": "B4"}',
        )

        time.sleep(1)
        stock_count = self.vending_machine.check_stock_by_code("B4")
        self.assertEqual(stock_count, 1)


if __name__ == "__main__":
    unittest.main()
