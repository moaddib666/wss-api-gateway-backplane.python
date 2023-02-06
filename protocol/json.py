import json

from .base import Message


class JsonMessage(Message):
    payload: dict

    @classmethod
    def from_amqp(cls, message) -> "Message":
        msg = super().from_amqp(message)
        try:
            msg.payload = json.loads(msg.payload)
        except Exception as err:
            raise cls.InvalidMessage() from err
        return msg
