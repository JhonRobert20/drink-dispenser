from threading import Timer
from typing import Dict, List, Optional

from src.domain.constants import (
    COIN_ENTITY_REQUIRED_ERROR,
    INVALID_COIN_ERROR,
    PRODUCT_NOT_FOUND_ERROR,
    SLOT_ENTITY_REQUIRED_ERROR,
    TRANSACTION_TIMER_NEEDED_ERROR,
    VENDING_MACHINE_ADD_PRODUCT_ERROR,
    MachineStatus,
    TransactionStatus,
)
from src.domain.entities.product import Product
from src.domain.entities.product_slot import ProductSlot
from src.domain.entities.transaction import Transaction
from src.domain.utils import PeekableProductsQueue
from src.domain.value_objects.coin import Coin


class VendingMachine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, slots: Optional[Dict[str, ProductSlot]], coins: List[Coin]):
        if self.__initialized:
            return
        self.__initialized = True

        if not isinstance(slots, dict):
            raise ValueError(SLOT_ENTITY_REQUIRED_ERROR)
        if not isinstance(coins, list):
            raise ValueError(COIN_ENTITY_REQUIRED_ERROR)

        self.slots = slots
        self.coins = coins
        self.coins_actual_transaction = []
        self.actual_transaction: Optional[Transaction] = None
        self.timer: Optional[Timer] = None
        self.machine_status = MachineStatus.AVAILABLE
        self.actual_slot_code: Optional[str] = None

    def add_product_to_slot(self, product: Product, slot_code: str) -> ProductSlot:
        self.machine_status = MachineStatus.BUSY
        slot: ProductSlot = self.get_slot_by_code(slot_code)
        if slot:
            next_product = slot.products.get_without_consume()
            if next_product and next_product.bar_code != product.bar_code:
                self.machine_status = MachineStatus.AVAILABLE
                raise ValueError(VENDING_MACHINE_ADD_PRODUCT_ERROR)
            slot.products.put(product)
            self.machine_status = MachineStatus.AVAILABLE
            return slot

        else:
            new_products_queue = PeekableProductsQueue([product])
            self.slots[slot_code] = ProductSlot(new_products_queue, slot_code)
            self.machine_status = MachineStatus.AVAILABLE
            return self.slots[slot_code]

    def __get_product_by_slot_code(self, slot_code: str) -> Optional[Product]:
        slot = self.get_slot_by_code(slot_code)
        if slot:
            return slot.products.get_without_consume()
        return None

    def check_product_availability(self, slot_code: str):
        product = self.__get_product_by_slot_code(slot_code)
        return product if product and product.is_valid() else None

    def select_product(self, slot_code: str):
        self.machine_status = MachineStatus.BUSY
        product = self.__get_product_by_slot_code(slot_code)
        if not product:
            self.machine_status = MachineStatus.AVAILABLE
            raise ValueError(PRODUCT_NOT_FOUND_ERROR)

        self.__start_timer()
        self.actual_transaction = Transaction(
            product, 0, TransactionStatus.PENDING, self.coins
        )
        self.actual_slot_code = slot_code
        return product.price

    def __start_timer(self):
        self.timer = Timer(5, self.__refund_coins_with_timer)
        self.timer.start()

    def reject_actual_transaction(self):
        if not self.actual_transaction or not self.timer:
            raise ValueError(TRANSACTION_TIMER_NEEDED_ERROR)

        status = self.actual_transaction.mark_as_cancelled()
        self.refund_coins()
        self.timer.cancel()
        self.actual_transaction = None
        return status

    def dispense_product(self, slot_code: str):
        product_to_expend = self.check_product_availability(slot_code)
        if not product_to_expend:
            # todo: send async message to admin
            return self.refund_coins()

        slot = self.get_slot_by_code(slot_code)
        paid_amount = round(
            sum([coin.denomination for coin in self.coins_actual_transaction]), 2
        )
        self.actual_transaction = Transaction(
            product_to_expend, paid_amount, TransactionStatus.PENDING, self.coins
        )
        try:
            coins_index_to_return = self.actual_transaction.validate_money()
            slot.products.get_if_exists()
            self.__remove_coins_from_machine(coins_index_to_return)
            status = self.actual_transaction.mark_as_completed()
            self.actual_transaction = None
            self.machine_status = MachineStatus.AVAILABLE
            return status
        except ValueError:
            return self.refund_coins()

    def __refund_coins_with_timer(self):
        # Todo: add logs
        return self.refund_coins()

    def refund_coins(self):
        index_to_remove = [i for i in range(len(self.coins_actual_transaction))]
        self.__remove_coins_from_machine(index_to_remove)
        self.machine_status = MachineStatus.AVAILABLE
        return TransactionStatus.REFUNDED

    def __remove_coins_from_machine(self, coins_index_to_return: List[int]):
        ordered_coins_index = sorted(coins_index_to_return, reverse=True)
        for index in ordered_coins_index:
            self.coins.pop(index)
        self.coins_actual_transaction = []

    def add_coin_to_transaction(self, coin: Coin):
        if not coin.is_valid():
            raise ValueError(INVALID_COIN_ERROR)

        self.coins.append(coin)
        self.coins_actual_transaction.append(coin)
        return True

    def get_slot_by_code(self, slot_code: str) -> Optional[ProductSlot]:
        if slot_code in self.slots:
            return self.slots[slot_code]
        return None

    def remove_slot(self, slot_code: str) -> Optional[ProductSlot]:
        if slot_code in self.slots:
            return self.slots.pop(slot_code)
        return None

    def check_stock_by_code(self, slot_code: str) -> int:
        if slot_code in self.slots:
            return self.slots[slot_code].products.qsize()
        return 0

    def list_product_stock(self):
        return {
            slot_code: {
                "quantity": slot.products.qsize(),
                "product": slot.products.get_name_without_consume(),
            }
            for slot_code, slot in self.slots.items()
        }

    def get_machine_status(self):
        return self.machine_status.value
