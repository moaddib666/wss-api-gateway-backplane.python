import abc


class Subscriber(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def subscribe(self):
        pass
