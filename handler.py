import json
import jsonpickle
import os
import boto3

# from state_manager.state_manager import StateManager
from state_manager.models import Book


def handle_add_book(event, context):
    print("Received new book request, starting to process...")
    body_str = event["body"]
    body = json.loads(body_str)
    book_source = body['bookSource']
    print(f"Book source to process: {book_source}")

    book = save_state(book_source)
    send_to_queue(book)

    return {
        "statusCode": 200
    }


def save_state(source: str) -> Book:
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")
    constr = f"postgresql://{user}:{password}@{host}/{dbname}"
    # m = StateManager(constr)
    # ret = m.add_book(source)
    # delete 2 lines below when 2 lines above will work properly
    ret = Book.from_source(source)
    ret.id = 1
    print("Book added successfully")
    return ret


def send_to_queue(book: Book):
    topic = os.environ.get("BOOKS_TOPIC")
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
