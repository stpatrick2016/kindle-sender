import os
import json

from .utils import get_project_root

class Configuration:

    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_engine: str
    topic_books: str
    persistency_enabled: bool
    file_prefix: str
    file_storage: str
    smtp_server: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    def __init__(self):
        self.db_host = os.environ.get("DB_HOST")
        self.db_user = os.environ.get("DB_USER")
        self.db_password = os.environ.get("DB_PASSWORD")
        self.db_engine = "postgres"
        self.db_name = os.environ.get("DB_NAME")
        self.topic_books = os.environ.get("BOOKS_TOPIC")
        self.persistency_enabled = os.environ.get("PERSISTENCY_ENABLED") == "1"
        self.file_prefix = os.environ.get("FILE_PREFIX") or "temp"
        self.file_storage = os.environ.get("FILE_STORAGE")
        self.smtp_server = os.environ.get("SMTP_SERVER")
        self.smtp_port = int(os.environ.get("SMTP_PORT") or 0) or 465
        self.smtp_user = os.environ.get("SMTP_USER")
        self.smtp_password = os.environ.get("SMTP_PASSWORD")

    def get_connection_string(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"

class LocalConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        configFile = os.path.join(get_project_root(), "appConfig.local.json")
        if os.path.isfile(configFile):
            with open(configFile, "r") as f:
                config = json.loads(f.read())

                self.db_host = config.get("DB_HOST") or self.db_host
                self.db_user = config.get("DB_USER") or self.db_user
                self.db_password = config.get("DB_PASSWORD") or self.db_password
                self.db_engine = config.get("DB_ENGINE") or self.db_engine
                self.db_name = config.get("DB_NAME") or self.db_name
                self.topic_books = config.get("BOOKS_TOPIC") or self.topic_books
                self.persistency_enabled = config.get("PERSISTENCY_ENABLED") == "1" or self.persistency_enabled
                self.file_prefix = config.get("FILE_PREFIX") or self.file_prefix
                self.file_storage = config.get("FILE_STORAGE") or self.file_storage
                self.smtp_server = config.get("SMTP_SERVER") or self.smtp_server
                self.smtp_port = int(config.get("SMTP_PORT") or 0) or self.smtp_port
                self.smtp_user = config.get("SMTP_USER") or self.smtp_user
                self.smtp_password = config.get("SMTP_PASSWORD") or self.smtp_password

