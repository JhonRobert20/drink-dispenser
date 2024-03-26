from typing import List

from src.domain.entities.transaction import Transaction
from src.domain.repositories.transaction import ITransactionRepository
from src.domain.value_objects.coin import Coin
from src.infrastructure.config.db_connection import MongodbManager
from src.infrastructure.persistence.models.transaction import TransactionModel
from src.infrastructure.utils import transaction_document_to_coins


class TransactionRepositoryImpl(ITransactionRepository):
    def __init__(self, mongodb_manager: MongodbManager):
        self.mongodb_manager = mongodb_manager
        self.collection_name = "transactions"

    def add_transaction(self, transaction: Transaction) -> None:
        transaction_model = TransactionModel(transaction)
        self.mongodb_manager.insert_document(
            transaction_model.to_dict(),
            coll_name=self.collection_name,
        )

    def get_coins_from_last_transaction(self) -> List[Coin]:
        last_transaction_data = self.mongodb_manager.find_document(
            self.collection_name, {}, find_one=False, sort=[("date", -1)]
        )
        if not last_transaction_data:
            return []
        return transaction_document_to_coins(last_transaction_data)
