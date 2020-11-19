import jsonpickle
import pytest

from state_manager.models import Book
from common.definitions.enums import BookState

def test_book_serialize():
    book = Book(id=1, state=BookState.new, source="aaa")
    s = jsonpickle.encode(book)
    assert s is not None
    
    res = jsonpickle.decode(s)
    assert res.id == book.id
    assert res.state == book.state
    assert res.source == book.source