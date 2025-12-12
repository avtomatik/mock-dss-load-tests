import psycopg

from core.constants import SQL_INSERT_DOCUMENT, SQL_SELECT_COUNT
from core.helpers import generate_random_content, generate_random_id


class PostgresClient:
    def __init__(self, url: str):
        self.url: str = url
        self.connection: psycopg.Connection | None = None

    def connect(self):
        if self.connection is None:
            self.connection = psycopg.connect(self.url)

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_signature_count_for_day(self, day: str) -> int:
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_COUNT, (day,))
            result = cursor.fetchone()
            return result[0] or 0

    def insert_document(self) -> None:
        self.connect()
        document_id = generate_random_id()
        content = generate_random_content()
        with self.connection.cursor() as cursor:
            cursor.execute(SQL_INSERT_DOCUMENT, (document_id, content))
