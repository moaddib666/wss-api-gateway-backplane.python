import socket


from protocol.base import Message, Metadata
from kombu import Producer, Queue, Connection, Exchange

from protocol.json import JsonMessage


class Publisher:
    def __init__(self):
        self.conn = Connection("amqp://user:bitnami@localhost:5672/")
        self.exchange = Exchange("ApiGatewayInbox", "direct")
        self.conn.connect()

    def publish(self, msg: JsonMessage):
        with self.conn.channel() as channel:
            producer = Producer(
                channel, serializer="json", exchange=self.exchange, auto_declare=True
            )
            producer.publish(
                msg.payload,
                retry=True,
                headers={
                    "sender": msg.metadata.sender,
                    "recipient": msg.metadata.recipient,
                },
            )

    def __del__(self):
        self.conn.close()


class EventPublisher(Publisher):
    def publish_event(self, recipient: str, event: "Event"):
        event.metadata.publisher_name = self.__class__.__name__
        msg = JsonMessage(
            metadata=Metadata(
                recipient=recipient,
                sender=socket.gethostname(),
            ),
            payload=event.dict(),
        )
        self.publish(msg)
