import random

from backplane.publisher.base import EventPublisher
from backplane.subscriber.handler import Handler
from backplane.subscriber.rmq import RMQSubscriber
from backplane.subscriber.router import Router
from protocol.events import EventMessage, Event


class SendCommand(Event):
    pass


class ShellOutputHandler(Handler):

    publisher = EventPublisher()

    def __call__(self, event: EventMessage, sender=None):
        print(
            f"Processing: {event.metadata.event_name} by handler {self.__class__.__name__}, data: {event.payload}"
        )
        if event.metadata.entity_id == "2" and sender:
            respond_event = SendCommand.create(
                {"cmd": "ls", "args": ["la"]}, str(random.randint(1, 99999)), "command"
            )
            print(f"Responding with event {respond_event} to {sender}")
            self.publisher.publish_event(recipient=sender, event=respond_event)


if __name__ == "__main__":

    Router.add("shellCommandOutput", ShellOutputHandler)
    subscriber = RMQSubscriber(queue="PythonTestQueue")
    subscriber.subscribe()
