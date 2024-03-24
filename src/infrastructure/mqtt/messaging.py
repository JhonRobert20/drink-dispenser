import paho.mqtt.client as mqtt
from src.domain.ports.mqtt_event_publisher import EventPublisher


class MqttEventPublisher(EventPublisher):
    def __init__(self, mqtt_client: mqtt.Client):
        self.mqtt_client = mqtt_client

    def publish(self, topic: str, message: str):
        self.mqtt_client.publish(topic, message)
