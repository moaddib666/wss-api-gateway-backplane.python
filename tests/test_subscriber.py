from unittest import TestCase

from backplane.subscriber.rmq import RMQSubscriber


class RMQSubscriberTestCase(TestCase):
    def test_subscribe(self):
        subscriber = RMQSubscriber(queue="PythonTestQueue")
        subscriber.subscribe()
