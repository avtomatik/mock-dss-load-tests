import json
from urllib.parse import urlparse

from gevent import monkey
from pika import (
    BasicProperties,
    BlockingConnection,
    ConnectionParameters,
    DeliveryMode,
    PlainCredentials,
)
from pika.channel import Channel

monkey.patch_all()


class RabbitMQClient:
    def __init__(self, url: str, queue_name: str = "test_queue"):
        self.url: str = url
        self.queue_name: str = queue_name
        self.connection: BlockingConnection | None = None
        self.channel: Channel = None

        parsed = urlparse(url)

        self.host = parsed.hostname
        self.port = parsed.port
        self.username = parsed.username
        self.password = parsed.password

    def connect(self):
        if self.connection is None:
            credentials = PlainCredentials(self.username, self.password)
            parameters = ConnectionParameters(
                host=self.host, port=self.port, credentials=credentials
            )
            self.connection = BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.channel = None

    def publish(self, payload: dict):
        if self.channel:
            body = json.dumps(payload).encode()
            properties = BasicProperties(delivery_mode=DeliveryMode.Persistent)
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=body,
                properties=properties,
            )
