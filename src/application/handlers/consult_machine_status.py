import logging

from src.application.commands.chec_vending_machine_status import (
    CheckVendingMachineCommand,
)
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher


class ConsultMachineStatusHandler:
    def __init__(
        self, vending_machine: VendingMachine, event_publisher: MqttEventPublisher
    ):
        self.vending_machine = vending_machine
        self.logger = logging.getLogger("ConsultMachineStatusHandler")
        self.event_publisher = event_publisher
        self.consult_machine_status_command = CheckVendingMachineCommand(
            vending_machine, self.logger
        )

    def handle(self, payload):
        self.logger.info("Handling consult machine status")
        self.logger.info(f"Payload: {payload}")
        machine_status = self.consult_machine_status_command.execute()
        self.logger.info("Machine status checked successfully.")
        self.event_publisher.publish("lcd/machine_status", machine_status)
