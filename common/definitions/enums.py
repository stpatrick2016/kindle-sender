import enum

class BookState(str, enum.Enum):
    new = "new"
    downloaded = "downloaded"
    done = "done"