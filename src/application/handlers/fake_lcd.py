import logging


class FakeLcdHandler:
    def __init__(self):
        self.logger = logging.getLogger("FakeLcdHandler")

    def handle(self, payload):
        self.logger.info("Handling Fake LCD")
        self.logger.info(f"Payload: {payload}")
