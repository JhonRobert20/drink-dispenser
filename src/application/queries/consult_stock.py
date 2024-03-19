from src.domain.entities.vending_machine import VendingMachine


class ConsultProductStockQuery:
    def __init__(self, vending_machine: VendingMachine):
        self.vending_machine = vending_machine

    def execute(self, slot_code: str) -> int:
        slot = self.vending_machine.get_slot_by_code(slot_code)
        if slot:
            return slot.products.qsize()
        else:
            return 0
