import json
from types import SimpleNamespace

from dataclasses import dataclass
from common.definitions.enums import BookState

@dataclass
class Book:
    id: int
    state: BookState
    source: str
    target: str

    @classmethod
    def from_source(cls, source: str):
        return cls(0, BookState.new, source)

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, data: str):
        return json.loads(data, object_hook=lambda d: Book(**d))
        