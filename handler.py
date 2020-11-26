import json
import jsonpickle
import os
import boto3
import asyncio

from state_manager.state_manager import StateManager
from state_manager.models import Book
from common.configuration import LocalConfiguration, Configuration
from downloader.downloader import Downloader
from sourcerer.parser import SourceParser

config = LocalConfiguration()

def handle_add_book(event, context):
    print("Received new book request, starting to process...")
    body = json.loads(event["body"])
    book_source = body['bookSource']
    print(f"Book source to process: {book_source}")

    parser = SourceParser(book_source)
    book = add_book(parser.get_download_url(), config)
    send_to_queue(book, config)

    return {
        "statusCode": 200
    }

def handle_download_book(event, context):
    print("Received download request...")
    loop = asyncio.get_event_loop()
    print(json.dumps(event))
    for record in event["Records"]:
        book: Book = jsonpickle.decode(record["body"])

        downloader = Downloader.factory(config.file_storage)
        loop.run_until_complete(downloader.download(book.source, f"{config.file_prefix}-{book.id}"))

        sm = StateManager(config.get_connection_string())
        book = sm.mark_downloaded(book)
        #send_to_queue(book, config)

    return {
        "statusCode": 200
    }

def add_book(source: str, config: Configuration) -> Book:
    m = StateManager(config.get_connection_string())
    ret = m.add_book(source)
    print("Book added successfully")
    return ret


def send_to_queue(book: Book, config: Configuration):
    topic = config.topic_books
    sns = boto3.client("sns")

    sns.publish(
        TopicArn=topic,
        Subject="book",
        Message=jsonpickle.encode(book),
        MessageAttributes={
            "state": {
                "DataType": "String",
                "StringValue": book.state
            }
        }
    )

if __name__ == "__main__":

    print("Welcome to manual execution of Kindle Books downloader")
    loop = asyncio.get_event_loop()
    selection = ""
    while selection != "0":
        print("Select one of the operations you would like to test")
        print("\t1. New book")
        print("\t2. Download book")
        print("\t0. Exit")

        selection = input("Your choice: ")
        if selection == "1":
            ev = {
                "body": "{\"bookSource\":\"http://flibusta.is/b/369935\"}"
            }
            handle_add_book(ev, "")
        elif selection == "2":
            book = Book(1, "new", "http://flibusta.is/b/369935/mobi")
            ev = {
                "Records":[
                    {
                        "body": jsonpickle.encode(book)
                    }
                ]
            }
            loop.run_until_complete(handle_download_book(ev, None))
    loop.close()