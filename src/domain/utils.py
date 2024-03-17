from typing import List

from src.domain.entities.product import Product


class PeekableProductsQueue:
    def __init__(self, products: List[Product]):
        self.queue = []
        if products:
            self.queue = products

    def get_without_consume(self):
        if not self.empty():
            return self.queue[0]
        else:
            return None

    def get_name_without_consume(self):
        if not self.empty():
            return self.queue[0].name
        else:
            return None

    def get_if_exists(self):
        if not self.empty():
            return self.queue.pop(0)
        else:
            return None

    def put(self, product: Product):
        self.queue.insert(0, product)

    def qsize(self):
        return len(self.queue)

    def empty(self):
        return len(self.queue) == 0
