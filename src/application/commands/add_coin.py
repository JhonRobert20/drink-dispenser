from logging import Logger
from typing import Optional

from src.domain.constants import INVALID_COIN_ERROR
from src.domain.entities.product import Product
from src.domain.entities.vending_machine import VendingMachine
from src.domain.value_objects.coin import Coin


class AddCoinCommand:
    def __init__(self, vending_machine: VendingMachine, logger: Logger):
        self.vending_machine = vending_machine
        self.logger = logger

    def execute(self, coin: Coin) -> Optional[Product]:
        try:
            return self.vending_machine.add_coin_to_transaction(coin)
        except ValueError:
            self.logger.error(INVALID_COIN_ERROR)
            return None
