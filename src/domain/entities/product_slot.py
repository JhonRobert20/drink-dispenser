from src.domain.utils import PeekableProductsQueue


class ProductSlot:
    def __init__(self, products: PeekableProductsQueue, code: str):
        self.products = products
        self.code = code
