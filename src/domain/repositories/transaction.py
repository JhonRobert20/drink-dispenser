from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.transaction import Transaction
from src.domain.value_objects.coin import Coin


class ITransactionRepository(ABC):
    @abstractmethod
    def add_transaction(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def get_coins_from_last_transaction(self) -> List[Coin]:
        pass
