from asyncio import Event
from typing import Any


class ValueWaiter(object):
    _event: Event
    _value: Any

    def __init__(self):
        self._event = Event()
        self._value = None

    async def wait(self) -> Any:
        await self._event.wait()
        self._event.clear()
        return self._value

    async def set(self, value: Any):
        self._value = value
        self._event.set()
