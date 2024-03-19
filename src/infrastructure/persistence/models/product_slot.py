from src.domain.entities.product_slot import ProductSlot
from src.infrastructure.persistence.models.product import ProductModel


class ProductSlotModel:
    def __init__(self, product_slot: ProductSlot):
        self.products = [
            ProductModel(product) for product in product_slot.products.queue
        ]
        self.code = product_slot.code

    def to_dict(self):
        return {
            "products": [product.to_dict() for product in self.products],
            "code": self.code,
        }
