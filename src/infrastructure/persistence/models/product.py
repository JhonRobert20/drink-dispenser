from src.domain.entities.product import Product


class ProductModel:
    def __init__(self, product: Product):
        self.name = product.name
        self.bar_code = product.bar_code
        self.expiration_date = product.expiration_date
