#!/usr/bin/env python

import asyncio
import dataclasses
import datetime
import json
import random
import time

import websockets

from protocol.events import Event, Metadata

TOKEN = "123321"


def build_message(eid) -> str:
    msg = Event(
        metadata=dict(
            entity_id=eid,
            entity_name="command",
            publisher_name="testPythonClient",
            event_name="shellCommandOutput",
            created=datetime.datetime.utcnow().isoformat(),
        ),
        payload={"necessary": "data"},
    )
    return msg.json()


async def hello():
    async with websockets.connect(
        "ws://127.0.0.1:8080", extra_headers={"Authorization": f"Bearer {TOKEN}"}
    ) as websocket:

        # name = random.randbytes(100)
        name = "hello"
        await websocket.send(name)
        print("> {}".format(name))

        greeting = await websocket.recv()
        print("< {}".format(greeting))
        for i in range(3):
            msg = build_message(i)
            await websocket.send(msg)
            print("> {}".format(msg))
            await websocket.recv()

        print("Wait for last event:")
        first_message = await websocket.recv()
        print("< LAST EVENT :{}".format(first_message))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello())
