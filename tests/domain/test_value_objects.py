import unittest
from domain.value_objects.coin import Coin


class TestCoin(unittest.TestCase):
    def test_coin_with_valid_denomination_and_currency(self):
        coin = Coin(denomination=1.00, currency="EUR")
        assert coin.is_valid() == True

    def test_coin_with_invalid_denomination(self):
        coin = Coin(denomination=0.03, currency="EUR")
        assert coin.is_valid() == False

    def test_coin_with_invalid_currency(self):
        coin = Coin(denomination=1.00, currency="USD")
        assert coin.is_valid() == False