import asyncio
import multiprocessing
from typing import Any

from .mqtt_rpc import MqttRpc
from .request import Request
from .response import Response, Status
from .topics import REQUESTS, RESPONSES


async def worker(app: MqttRpc, topic: str) -> None:
    async with app.client as client:
        async with client.unfiltered_messages() as messages:
            await client.subscribe(
                "/".join(filter(None, [app.name, REQUESTS, topic, "#"]))
            )

            async for message in messages:
                request = Request.from_json(message.payload)

                task = app.tasks[request.task]

                try:
                    result = task(*request.args, **request.kwargs)
                    status = Status.SUCCESS
                except Exception as error:
                    result = error.__dict__
                    status = Status.FAILURE

                response = Response(request.id, result, status)

                await client.publish(
                    "/".join([app.name, RESPONSES, request.origin]), response.to_json()
                )


def run_worker(app: MqttRpc, topic: str) -> Any:
    asyncio.run(worker(app, topic))


def main(app: MqttRpc, topic: str, concurrency: int | None = None) -> None:
    pool = multiprocessing.Pool(processes=concurrency)
    for _ in range(getattr(pool, "_processes", 1)):
        pool.apply_async(run_worker(app, topic))
    pool.join()
