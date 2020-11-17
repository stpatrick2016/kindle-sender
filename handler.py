from __future__ import print_function

import json


def handle_add_book(event, context):
    print("Received new book request, starting to process...")
    body_str = event["body"]
    print("Body is: " + body_str)
    body = json.loads(body_str)
    book_source = body['bookSource']
    print("Book source to process: " + book_source)

    return {
        "statusCode": 200
    }
