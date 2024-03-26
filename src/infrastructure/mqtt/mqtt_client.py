import os
import random

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from src.application.handlers.add_product import AddProductHandler
from src.application.handlers.consult_machine_status import ConsultMachineStatusHandler
from src.application.handlers.consult_stock import ConsultStockHandler
from src.application.handlers.product_selection import ProductSelectionHandler
from src.domain.entities.vending_machine import VendingMachine
from src.infrastructure.mqtt.messaging import MqttEventPublisher

vending_machine_instance = VendingMachine({}, [])


def configure_handlers(vending_machine, event_publisher=None):
    product_selection_handler = ProductSelectionHandler(
        vending_machine, event_publisher
    )
    add_product_handler = AddProductHandler(vending_machine, event_publisher)
    consult_stock_handler = ConsultStockHandler(vending_machine, event_publisher)
    consult_machine_status_handler = ConsultMachineStatusHandler(
        vending_machine, event_publisher
    )

    return {
        "vending_machine/selections": product_selection_handler.handle,
        "vending_machine/add": add_product_handler.handle,
        "vending_machine/consult_stock": consult_stock_handler.handle,
        "vending_machine/consult_status": consult_machine_status_handler.handle,
    }


def start_and_configure_mqtt_client(
    logger,
    broker="mqtt.example.com",
    port=1883,
    vending_machine=None,
):
    client_id = f"python-mqtt-{random.randint(0, 1000)}"
    mqtt_client = mqtt.Client(
        client_id=client_id, callback_api_version=CallbackAPIVersion.VERSION2
    )
    mqtt_user = os.environ.get("MQTT_USER", "user")
    mqtt_password = os.environ.get("MQTT_PASSWORD", "password")
    mqtt_client.username_pw_set(mqtt_user, mqtt_password)

    event_publisher = MqttEventPublisher(mqtt_client)
    topic_handlers = configure_handlers(vending_machine, event_publisher)

    def on_connect(client, userdata, flags, rc, *args, **kwargs):
        if rc == 0:
            logger.info("Connected to broker")
        else:
            logger.error(f"Connection failed with code {rc}")

    def subscribe_topics(client):
        def on_message(client, userdata, msg):
            handler = topic_handlers.get(msg.topic)
            logger.info(
                f"Received message {msg.payload.decode('utf-8')} on topic {msg.topic}"
            )
            if handler:
                handler(msg.payload.decode("utf-8"))
            else:
                logger.warning(f"No handler for topic {msg.topic}")

        for topic in topic_handlers.keys():
            mqtt_client.subscribe(topic)
            mqtt_client.on_message = on_message

    mqtt_client.on_connect = on_connect
    mqtt_client.connect(host=broker, port=port, keepalive=60)
    mqtt_client.enable_logger(logger)
    subscribe_topics(mqtt_client)
    mqtt_client.loop_start()
    return mqtt_client
