import abc


class Handler(abc.ABC):

    target: str

    def __call__(self, event: "EventMessage", sender=None):
        pass


class DefaultHandler(Handler):
    target = ""

    def __call__(self, event: "EventMessage", sender=None):
        print("Default handler has been asigned to this task", event, sender)
