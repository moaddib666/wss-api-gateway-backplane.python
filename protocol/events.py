import datetime
import json
from json import JSONDecodeError

import pydantic
from pydantic import BaseModel

from protocol.json import JsonMessage


class Metadata(BaseModel):
    entity_id: str
    entity_name: str
    publisher_name: str
    event_name: str
    created: datetime.datetime


class Event(BaseModel):
    metadata: Metadata
    payload: dict

    @classmethod
    def create(cls, payload, entity_id, entity_name):
        return cls(
            metadata=Metadata(
                entity_id=entity_id,
                entity_name=entity_name,
                publisher_name="unknown",
                event_name=cls.__name__,
                created=datetime.datetime.now(),
            ),
            payload=payload,
        )


class EventMessage(JsonMessage, BaseModel):
    payload: Event

    @classmethod
    def from_amqp(cls, message) -> "Message":
        try:
            return cls(metadata=message.headers, payload=json.loads(message.body))
        except (pydantic.ValidationError, JSONDecodeError) as err:
            raise cls.InvalidMessage(message.body) from err

    @property
    def event_name(self) -> str:
        return self.payload.metadata.event_name
