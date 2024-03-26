from src.infrastructure.persistence.repositori_impl.product_slot import (
    ProductSlotRepositoryImpl,
)
from src.tests.base import TestBase


class TestModels(TestBase):
    def test_can_create_product_slot_in_mongo(self):
        product_slot_repo = ProductSlotRepositoryImpl(self.mongo_db)
        product_slot_repo.save_product_slot(self.slot_coke)
        product_slot = product_slot_repo.get_product_slot_by_code(self.slot_coke.code)
        self.assertEqual(self.slot_coke.code, product_slot.code)
        first_product_repo = product_slot.products.get_without_consume()
        first_product_actual = product_slot.products.get_without_consume()
        self.assertEqual(first_product_repo.name, first_product_actual.name)
        self.assertEqual(first_product_repo.bar_code, first_product_actual.bar_code)
        self.assertEqual(
            first_product_repo.expiration_date, first_product_actual.expiration_date
        )
        self.assertEqual(first_product_repo.price, first_product_actual.price)

    def test_can_list_product_slots(self):
        product_slot_repo = ProductSlotRepositoryImpl(self.mongo_db)
        product_slot_repo.save_product_slot(self.slot_coke)
        product_slot_repo.save_product_slot(self.slot_to_expensive)
        product_slots = product_slot_repo.list_product_slots()
        self.assertEqual(len(product_slots), 2)
        self.assertEqual(
            product_slots[self.slot_coke.code].products.get_without_consume().bar_code,
            self.slot_coke.products.get_without_consume().bar_code,
        )
