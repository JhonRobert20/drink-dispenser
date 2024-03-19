from datetime import datetime

from src.domain.entities.product import Product
from src.domain.utils import PeekableProductsQueue


def document_to_product(document) -> Product:
    expiration_date = datetime.strptime(document["expiration_date"], "%Y-%m-%d").date()
    return Product(
        name=document["name"],
        bar_code=document["bar_code"],
        expiration_date=expiration_date,
        price=document["price"],
    )


def products_documents_to_product_slot(product_documents) -> PeekableProductsQueue:
    return PeekableProductsQueue(
        [
            document_to_product(product_document)
            for product_document in product_documents
        ]
    )
