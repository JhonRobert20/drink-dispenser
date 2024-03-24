import logging

from src.domain.entities.vending_machine import VendingMachine


class ConsultMachineStatusHandler:
    def __init__(self, vending_machine: VendingMachine, event_publisher=None):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("ConsultMachineStatusHandler")
        self.event_publisher = event_publisher

    def set_event_publisher(self, event_publisher):
        self.event_publisher = event_publisher

    def handle(self, payload):
        self.logger.info("Handling consult machine status")
