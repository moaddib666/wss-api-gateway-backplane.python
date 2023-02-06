from typing import Type

from .handler import DefaultHandler, Handler


class Router:
    default_handler = DefaultHandler()

    mapping = {"": default_handler}

    @classmethod
    def add(cls, task: str, handler: Type[Handler]):
        cls.mapping[task] = handler()

    @classmethod
    def resolve(cls, task: str) -> Handler:
        return cls.mapping.get(task, cls.default_handler)
