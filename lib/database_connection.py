
import psycopg
from psycopg.rows import dict_row
import os

class DatabaseConnection:

    # new line for test database
    DATABASE_NAME = os.getenv("DATABASE_NAME", "book_store")

    # When you're running Flask normally on your Mac, it uses localhost.
    # When Flask runs inside Docker, it uses the database host specified in your Dockerfile.

    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")

    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg.connect(
                f"postgresql://{self.DATABASE_HOST}/{self.DATABASE_NAME}",
                row_factory=dict_row)
        except psycopg.OperationalError:
            raise Exception(f"Couldn't connect to the database {self.DATABASE_NAME}! " \
                    f"Did you create it using `createdb {self.DATABASE_NAME}`?")

    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    CONNECTION_MESSAGE = '' \
        'DatabaseConnection.exec_params: Cannot run a SQL query as ' \
        'the connection to the database was never opened. Did you ' \
        'make sure to call first the method DatabaseConnection.connect` ' \
        'in your app.py file (or in your tests)?'

    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)