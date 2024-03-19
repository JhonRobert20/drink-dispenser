from typing import List, Optional

from src.domain.entities.product_slot import ProductSlot
from src.domain.repositories.product_slot import IProductSlotRepository
from src.infrastructure.config.db_connection import MongodbManager
from src.infrastructure.persistence.models.product_slot import ProductSlotModel
from src.infrastructure.utils import products_documents_to_product_slot


class ProductSlotRepositoryImpl(IProductSlotRepository):
    def __init__(self, mongodb_manager: MongodbManager):
        self.mongodb_manager = mongodb_manager
        self.collection_name = "product_slots"

    def save_product_slot(self, product_slot: ProductSlot) -> None:
        product_slot_model = ProductSlotModel(product_slot)
        self.mongodb_manager.upsert_document(
            product_slot_model.to_dict(),
            coll_name=self.collection_name,
            unique_field_name="code",
        )

    def get_product_slot_by_code(self, code: str) -> Optional[ProductSlot]:
        product_slot_data = self.mongodb_manager.find_document(
            self.collection_name, {"code": code}, find_one=True
        )
        if product_slot_data:
            products = products_documents_to_product_slot(product_slot_data["products"])
            return ProductSlot(code=product_slot_data["code"], products=products)
        return None

    def list_product_slots(self) -> List[ProductSlot]:
        product_slots_data = self.mongodb_manager.find_document(
            self.collection_name, {}, find_one=False
        )
        product_slots = []
        for product_slot_data in product_slots_data:
            products = products_documents_to_product_slot(product_slot_data["products"])
            product_slots.append(
                ProductSlot(code=product_slot_data["code"], products=products)
            )
        return product_slots
