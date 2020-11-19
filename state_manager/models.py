from dataclasses import dataclass
from common.definitions.enums import BookState

@dataclass
class Book:
    id: int
    state: BookState
    source: str

    @classmethod
    def from_source(cls, source: str):
        return cls(0, BookState.new, source)

        