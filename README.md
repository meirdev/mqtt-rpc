# MQTT RPC

Implementation of RPC over MQTT.

## Usage

Run the broker:

```bash
./broker/run.sh
```

Create a new app instance (`app.py`):

```python
from mqtt_rpc import mqtt_rpc

app = mqtt_rpc.MqttRpc("mytest", ["tasks"], {"hostname": "localhost"})
```

Run the worker:

```bash
python -m mqtt_rpc --app app.app worker
```

Write a task (`tasks.py`):

```python
from app import app

@app.task
def sum(a, b) -> int:
    return a + b
```

Send a task to the worker:

```python
import asyncio

import tasks

async def main() -> None:
    res = await tasks.sum.apply_sync(args=[1, 3])
    print(await res.get())

asyncio.run(main())
```

Result:

```text
Response(id='63408401-f95d-437b-9810-4e5a2b3335ae', result=4, status=<Status.SUCCESS: 2>)
```
