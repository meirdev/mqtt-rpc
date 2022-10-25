import asyncio
import importlib
import os
from typing import Any, Callable, ParamSpec, TypeVar

import asyncio_mqtt

from .response import Response
from .task import Task
from .topics import RESPONSES

T = TypeVar("T")
P = ParamSpec("P")


class MqttRpc:
    def __init__(
        self, name: str, imports: list[str], client_conf: dict[str, Any]
    ) -> None:
        self._name = name
        self._imports = imports
        self._client_conf = client_conf
        self._node = os.uname().nodename
        self._tasks: dict[str, Task] = {}
        self._responses: dict[str, Response] = {}

        self._client: asyncio_mqtt.Client | None = None
        self._cond = asyncio.Condition()

    @property
    def client(self) -> asyncio_mqtt.Client:
        if not self._client:
            self._client = asyncio_mqtt.Client(**self._client_conf)
        return self._client

    @property
    def imports(self) -> list[str]:
        return self._imports

    @property
    def name(self) -> str:
        return self._name

    @property
    def node(self) -> str:
        return self._node

    @property
    def tasks(self) -> dict[str, Any]:
        return self._tasks

    @property
    def cond(self) -> asyncio.Condition:
        return self._cond

    @property
    def responses(self) -> dict[str, Response]:
        return self._responses

    async def read_responses(self) -> None:
        async with self.client.unfiltered_messages() as messages:
            await self.client.subscribe(
                "/".join([self._name, RESPONSES, self._node, "#"])
            )

            async for message in messages:
                response = Response.from_json(message.payload)
                self._responses[response.id] = response

                async with self._cond:
                    self._cond.notify_all()

    async def wait_to_responses(self, request_id: str) -> Response:
        while True:
            async with self._cond:
                await self._cond.wait()

                if request_id in self._responses:
                    return self._responses.pop(request_id)

    async def connection(self) -> asyncio_mqtt.Client:
        try:
            self.client._connected.result()
        except asyncio.InvalidStateError:
            await self.client.connect()
            asyncio.create_task(self.read_responses())

        return self.client

    def load_imports(self) -> None:
        for i in self._imports:
            importlib.import_module(i)

    def task(self, function: Callable[P, T]) -> Task:
        self._tasks[function.__name__] = Task(self, function)
        return self._tasks[function.__name__]


def get_app(app: str) -> MqttRpc:
    module_name, variable_name = app.rsplit(".", 1)

    module = importlib.import_module(module_name)

    return getattr(module, variable_name)
