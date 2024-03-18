from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_product_by_bar_code(self, bar_code: str) -> Product:
        pass

    @abstractmethod
    def list_products(self) -> List[Product]:
        pass

    @abstractmethod
    def remove_product(self, bar_code: str) -> None:
        pass
