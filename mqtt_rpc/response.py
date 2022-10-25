import dataclasses
import enum
from typing import Any

import dataclasses_json


class Status(enum.IntEnum):
    PENDING = 0
    STARTED = 1
    SUCCESS = 2
    FAILURE = 3


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Response:
    id: str
    result: Any
    status: Status = Status.PENDING
