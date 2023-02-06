from pydantic import BaseModel


class Metadata(BaseModel):
    recipient: str
    sender: str


class Message(BaseModel):
    metadata: Metadata
    payload: bytes

    @classmethod
    def from_amqp(cls, message) -> "Message":
        try:
            meta = Metadata(
                recipient=message.headers["recipient"],
                sender=message.headers["sender"],
            )
        except Exception as err:
            raise cls.InvalidMessage(message.headers) from err

        return cls(metadata=meta, payload=message.body)

    class InvalidMessage(Exception):
        pass

    @property
    def event_name(self) -> str:
        return "testEvent"
