from src.domain.entities.product import Product


class ProductModel:
    def __init__(self, product: Product):
        self.name = product.name
        self.bar_code = product.bar_code
        self.expiration_date = product.expiration_date.isoformat()
        self.price = product.price

    def to_dict(self):
        return {
            "name": self.name,
            "bar_code": self.bar_code,
            "expiration_date": self.expiration_date,
            "price": self.price,
        }
