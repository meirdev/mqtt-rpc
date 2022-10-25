import dataclasses
import uuid
from typing import Any

import dataclasses_json


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Request:
    task: str
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    origin: str
    id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
