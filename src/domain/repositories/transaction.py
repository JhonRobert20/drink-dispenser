from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.transaction import Transaction


class ITransactionRepository(ABC):
    @abstractmethod
    def add_transaction(self, transaction: Transaction) -> None:
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        pass

    @abstractmethod
    def list_transactions(self) -> List[Transaction]:
        pass
