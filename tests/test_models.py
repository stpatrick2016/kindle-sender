import pytest

from state_manager.models import Book
from common.definitions.enums import BookState

def test_book_serialize():
    book = Book(id=1, state=BookState.new, source="aaa")
    s = book.to_json()
    assert s is not None
    
    res = Book.from_json(s)
    assert res.id == book.id
    assert res.state == book.state
    assert res.source == book.source