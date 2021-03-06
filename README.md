# Send books from Web to Kindle

[![Build status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiZ0RQdTZVRS8raHZxZjdpbnlvbkJKamQvNHdQaVRUYnpCQjgvUTZsNUNKb1R6NEx2RUZ0VW04bGJkdzd1Nlc0LzNaY3FGTFZLbVV6VEtNN1dWUXpCWWRBPSIsIml2UGFyYW1ldGVyU3BlYyI6IkROT3VMTmdOQWd0aUkzWE0iLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)](https://eu-central-1.console.aws.amazon.com/codesuite/codebuild/238645272082/projects/kindle-books-release/history?region=eu-central-1)

### Goal
The purpose of this **overengineered** project is to learn AWS and Python, nothing more. For that, I took a little practical idea of having an ability to send a book from [unnamed] site straight to my kindle and converted it to huge learning project.

The following technologies and languages were used during development:
* [Python](https://www.python.org)
* [AWS](https://aws.amazon.com), specifically:
  * [Lambda](https://aws.amazon.com/lambda)
  * [CodeBuild](https://aws.amazon.com/codebuild)
  * [API Gateway](https://aws.amazon.com/api-gateway)
  * [IAM](https://aws.amazon.com/iam)
  * [RDS](https://aws.amazon.com/rds), specifically [PostgreSQL](https://www.postgresql.org).
  * [S3](https://aws.amazon.com/s3)
  * [Secrets Manager](https://aws.amazon.com/secrets-manager)
  * [SNS](https://aws.amazon.com/sns) (Simple Notifications Service)
  * [SQS](https://aws.amazon.com/sqs) (Simple Queue Service)
* [Serverless](https://www.serverless.com)

### Architecture
The solution consists of:
* Lambda triggered by API Gateway with POST to /books, which accepts JSON payload with which book to download and where to send it.
* Lambda that listens on queue, downloads a book and stores it on S3
* Lambda that listens on queue, and sends a book as attachment to mail address using SMTP server
* [Optional] PostgreSQL database that stores current state
* [Not implemented] Browser plugin that sends links to /books and initiates the whole process

![Architecture](doc/architecture.png)
