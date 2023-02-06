from kombu import Exchange, Queue, Connection
from kombu.mixins import ConsumerProducerMixin

from protocol.base import Message
from protocol.events import EventMessage
from .base import Subscriber
from .router import Router


class RMQSubscriber(Subscriber):

    exchange = Exchange("ApiGatewayOutbox", "topic", durable=True)
    router: Router = Router

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue(queue, exchange=self.exchange)
        self.conn = Connection("amqp://user:bitnami@localhost:5672/")

    def on_message(self, body, message):
        print("RECEIVED MESSAGE: {0!r}".format(body))
        message.ack()

    def subscribe(self):
        worker = self.construct_worker()
        worker.run()

    def construct_worker(self) -> "Worker":
        return Worker(self.conn, self.queue, self.router)


class Worker(ConsumerProducerMixin):

    dto: Message = EventMessage

    def __init__(self, connection, queue, router):
        self.connection = connection
        self.queue = queue
        self.router = router

    def get_consumers(self, consumer, channel):
        return [
            consumer(
                queues=[self.queue],
                on_message=self.on_request,
                accept={"application/json"},
                prefetch_count=1,
            )
        ]

    def on_request(self, message):
        try:
            msg = self.dto.from_amqp(message)
        except self.dto.InvalidMessage:
            print(f"invalid formatted message {message.body} headers:{message.headers}")
            message.ack()
            return

        try:
            handler = self.router.resolve(msg.event_name)
            handler(msg.payload, sender=msg.metadata.sender)
        except Exception as err:
            print(f"Exception while msg processing: {err}")
        finally:
            message.ack()
