import datetime
from domain.constants import PRODUCT_EXPIRATION_FORMAT_ERROR


class Product:
    def __init__(self, name: str, code: str, price: float, expiration_date: datetime.date):
        if not isinstance(expiration_date, datetime.date):
            raise ValueError(PRODUCT_EXPIRATION_FORMAT_ERROR)

        self.name = name
        self.code = code
        self.price = price
        self.expiration_date = expiration_date

    def __str__(self):
        return f"{self.name} - {self.price}"

    def is_valid(self):
        return self.expiration_date > datetime.date.today()
