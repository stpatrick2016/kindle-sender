import psycopg2

from .models import Book
from common.definitions.enums import BookState

class StateManager:
    def __init__(self, connection: str):
        self._connection = connection
        self._is_enabled = True

    def set_enabled(self, is_enabled: bool):
        self._is_enabled = is_enabled

    def add_book(self, source: str) -> Book:
        book = Book.from_source(source)

        if self._is_enabled:
            self._create_books_table()
            conn = None
            try:
                print(f"Adding books with source {book.source} to database")
                conn = psycopg2.connect(self._connection)
                cur = conn.cursor()

                sql = "insert into books(state, source) values %s returning id"
                cur.execute(sql, [(book.state, book.source)])
                book.id = cur.fetchone()[0]
                conn.commit()
                cur.close()
                print("Books was added successfully")
            except(Exception, psycopg2.DatabaseError) as error:
                print(f"Failed to add book: {error}")
                raise error
            finally:
                if conn is not None:
                    conn.close()
        else:
            print("Saving state is disabled")
        
        return book

    def _create_books_table(self):
        command = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            state VARCHAR(10),
            source VARCHAR(255)
        )
        """

        conn = None
        try:
            print("Creating table books if missing")
            conn = psycopg2.connect(self._connection)
            cur = conn.cursor()
            cur.execute(command)
            cur.close()
            conn.commit()
            print("Creation completed successfully")
        except(Exception, psycopg2.DatabaseError) as error:
            print(f"Unable to create table: {error}")
            raise error
        finally:
            if conn is not None:
                conn.close()



