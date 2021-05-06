import json
import os
import boto3
import asyncio

from state_manager.state_manager import StateManager
from state_manager.models import Book, BookState
from common.configuration import LocalConfiguration, Configuration
from sourcerer.parser import SourceParser
from transport.depot import Depot

config = LocalConfiguration()


def handle_add_book(event, context):
    print("Received new book request, starting to process...")
    body = json.loads(event["body"])
    book_source = body['bookSource']
    address = body["address"]
    print(f"Book source to process: {book_source} to be sent to {address}")

    parser = SourceParser(book_source)
    book = add_book(parser.get_download_url(), address, config)
    send_to_queue(book, config)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Credentials": True,
        }
    }


def handle_download_book(event, context):
    print("Received download request...")
    for record in event["Records"]:
        body = json.loads(record["body"])
        book: Book = Book.from_json(body["Message"])
        if book.state == BookState.new:
            depot = Depot.from_http_to_s3(book.source, config.file_storage, f"{config.file_prefix}-{book.id}.mobi")
            asyncio.run(depot.dispatch())
            book.source = config.file_storage + "/" + f"{config.file_prefix}-{book.id}.mobi"

            sm = StateManager(config.get_connection_string())
            book = sm.mark_downloaded(book)
            send_to_queue(book, config)
        else:
            print(f"Ignoring book with state {book.state}")

    return {
        "statusCode": 200
    }


def handle_send_book(event, context):
    print("Reseved book to send")
    for record in event["Records"]:
        body = json.loads(record["body"])
        book: Book = Book.from_json(body["Message"])
        if book.state == BookState.downloaded:
            depot = Depot.from_s3_to_mail(
                config.file_storage,
                f"{config.file_prefix}-{book.id}.mobi",
                book.target,
                config.smtp_server,
                config.smtp_port,
                config.smtp_user,
                config.smtp_password
            )
            asyncio.run(depot.dispatch())

            sm = StateManager(config.get_connection_string())
            book = sm.mark_done(book)
            send_to_queue(book, config)
        else:
            print(f"Ignoring book with incompatible state: {book.state}")


def add_book(source: str, target: str, config: Configuration) -> Book:
    m = StateManager(config.get_connection_string())
    ret = m.add_book(source, target)
    print("Book added successfully")
    return ret


def send_to_queue(book: Book, config: Configuration):
    print("Sending book to topic")
    topic = config.topic_books
    sns = boto3.client("sns")

    sns.publish(
        TopicArn=topic,
        Subject="book",
        Message=book.to_json(),
        MessageAttributes={
            "state": {
                "DataType": "String",
                "StringValue": book.state
            }
        }
    )


def simulateSqsMessage(book: Book) -> dict:
    body = {
        "Message": book.to_json()
    }
    ev = {
        "Records": [
            {
                "body": json.dumps(body)
            }
        ]
    }
    return ev


if __name__ == "__main__":

    print("Welcome to manual execution of Kindle Books downloader")
    selection = ""
    while selection != "0":
        print("Select one of the operations you would like to test")
        print("\t1. New book")
        print("\t2. Download book")
        print("\t3. Send book")
        print("\t0. Exit")

        selection = input("Your choice: ")
        if selection == "1":
            ev = {
                "body": "{\"bookSource\":\"http://flibusta.is/b/369935\", \"address\":\"saint.patricius@gmail.com\"}"
            }
            handle_add_book(ev, "")
        elif selection == "2":
            book = Book(1, BookState.new, "http://flibusta.is/b/369935/mobi", "")
            ev = simulateSqsMessage(book)
            handle_download_book(ev, None)
        elif selection == "3":
            book = Book(1, BookState.downloaded, "arn:aws:s3:::books-download-dev/book.mobi",
                        "saint.patricius@gmail.com")
            ev = simulateSqsMessage(book)
            handle_send_book(ev, None)
