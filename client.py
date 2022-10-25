import asyncio

import tasks


async def main():
    a = await tasks.hello.apply_sync()
    print(await a.get())

    b = await tasks.sum.apply_sync(args=[1, 3])
    print(await b.get())


asyncio.run(main())
