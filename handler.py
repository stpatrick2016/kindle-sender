import json
import jsonpickle
import os
import boto3

from state_manager.state_manager import StateManager
from state_manager.models import Book
from common.configuration import LocalConfiguration, Configuration


def handle_add_book(event, context):
    print("Received new book request, starting to process...")
    body_str = event["body"]
    body = json.loads(body_str)
    book_source = body['bookSource']
    print(f"Book source to process: {book_source}")

    config = LocalConfiguration()
    book = save_state(book_source, config)
    send_to_queue(book, config)

    return {
        "statusCode": 200
    }


def save_state(source: str, config: Configuration) -> Book:
    m = StateManager(config.get_connection_string())
    ret = m.add_book(source)
    # delete 2 lines below when 2 lines above will work properly
    # ret = Book.from_source(source)
    # ret.id = 1
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
                "StringValue": "new"
            }
        }
    )

if __name__ == "__main__":
    ev = {
        "body": "{\"bookSource\":\"http://flibusta.is/b/369935\"}"
    }
    handle_add_book(ev, "")