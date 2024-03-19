from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.product import Product
from src.domain.entities.product_slot import ProductSlot


class IProductSlotRepository(ABC):
    @abstractmethod
    def save_product_slot(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_product_slot_by_code(self, bar_code: str) -> Optional[ProductSlot]:
        pass

    @abstractmethod
    def list_product_slots(self) -> List[ProductSlot]:
        pass
