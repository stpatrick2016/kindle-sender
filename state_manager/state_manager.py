import psycopg2
import time

from .models import Book
from common.definitions.enums import BookState
from common.configuration import Configuration

class StateManager:
    def __init__(self, connection: str):
        self._connection = connection
        self._config = Configuration()

    def add_book(self, source: str, target: str) -> Book:
        book = Book.from_source(source)
        book.id = round(time.time())
        book.target = target

        if self._config.persistency_enabled:
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
    
    def mark_downloaded(self, book: Book) -> Book:
        print("Updating book status to downloaded")
        book.state = BookState.downloaded
        self._save_book_in_db(book)
        return book

    def mark_done(self, book: Book) -> Book:
        print("Updating book status to done")
        book.state = BookState.done
        self._save_book_in_db(book)
        return book

    def _save_book_in_db(self, book: Book):
        if self._config.persistency_enabled:
            conn = None
            try:
                print(f"Marking book {book.id} as downloaded")
                conn = psycopg2.connect(self._connection)
                cur = conn.cursor()

                sql = "update books set state = %s where id = %s"
                cur.execute(sql, [(book.state, book.id)])
                print(f"Updates {cur.rowcount} rows")
                conn.commit()
                cur.close()
                print("Books was added successfully")
            except(Exception, psycopg2.DatabaseError) as error:
                print(f"Failed to add book: {error}")
                raise error
            finally:
                if conn is not None:
                    conn.close()


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



