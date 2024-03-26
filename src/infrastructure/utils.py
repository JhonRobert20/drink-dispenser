from datetime import datetime
from typing import List

from src.domain.entities.product import Product
from src.domain.utils import PeekableProductsQueue
from src.domain.value_objects.coin import Coin


def document_to_product(document) -> Product:
    expiration_date = datetime.strptime(document["expiration_date"], "%Y-%m-%d").date()
    return Product(
        name=document["name"],
        bar_code=document["bar_code"],
        expiration_date=expiration_date,
        price=document["price"],
    )


def document_to_coin(document) -> Coin:
    return Coin(
        denomination=document["denomination"],
        currency=document["currency"],
    )


def products_documents_to_product_slot(product_documents) -> PeekableProductsQueue:
    return PeekableProductsQueue(
        [
            document_to_product(product_document)
            for product_document in product_documents
        ]
    )


def transaction_document_to_coins(transaction_document) -> List[Coin]:
    return [
        document_to_coin(coin_document)
        for coin_document in transaction_document["coins"]
    ]
