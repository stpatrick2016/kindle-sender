import os
import jsonpickle

from .utils import get_project_root

class Configuration:

    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_engine: str
    topic_books: str

    def __init__(self):
        self.db_host = os.environ.get("DB_HOST")
        self.db_user = os.environ.get("DB_USER")
        self.db_password = os.environ.get("DB_PASSWORD")
        self.db_engine = "postgres"
        self.db_name = os.environ.get("DB_NAME")
        self.topic_books = os.environ.get("BOOKS_TOPIC")

    def get_connection_string(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"

class LocalConfiguration(Configuration):
    def __init__(self):
        super().__init__()
        configFile = os.path.join(get_project_root(), "appConfig.local.json")
        if os.path.isfile(configFile):
            with open(configFile, "r") as f:
                config = jsonpickle.decode(f.read())

                self.db_host = config.get("DB_HOST") or self.db_host
                self.db_user = config.get("DB_USER") or self.db_user
                self.db_password = config.get("DB_PASSWORD") or self.db_password
                self.db_engine = config.get("DB_ENGINE") or self.db_engine
                self.db_name = config.get("DB_NAME") or self.db_name
                self.topic_books = config.get("BOOKS_TOPIC") or self.topic_books

