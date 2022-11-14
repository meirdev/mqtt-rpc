from typing import TYPE_CHECKING, Any, Callable

from .request import Request
from .response import Response
from .topics import ALL, REQUESTS

if TYPE_CHECKING:
    from .mqtt_rpc import MqttRpc


class Task:
    def __init__(
        self,
        app: "MqttRpc",
        function: Callable[..., Any],
        topic: list[str] | None = None,
    ) -> None:
        self._app = app
        self._function = function
        self._topic = topic

    @property
    def app(self) -> "MqttRpc":
        return self._app

    @property
    def topic(self) -> list[str] | None:
        return self._topic

    async def apply_sync(
        self, args: tuple[Any, ...] | None = None, kwargs: dict[str, Any] | None = None
    ) -> "TaskRequest":
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = dict()

        connection = await self._app.connection()

        request = Request(
            task=self._function.__name__,
            args=args,
            kwargs=kwargs,
            origin=self._app.node,
        )

        await connection.publish(
            "/".join([self._app.name, REQUESTS, ALL]), request.to_json(), qos=2
        )

        task_request = TaskRequest(self, request)

        return task_request

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._function(*args, **kwargs)


class TaskRequest:
    def __init__(self, task: Task, request: Request) -> None:
        self._task = task
        self._request = request

    async def get(self) -> Response:
        return await self._task.app.wait_to_responses(self._request.id)
