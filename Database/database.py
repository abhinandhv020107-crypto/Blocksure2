import sqlite3
import os

DATABASE_NAME = "blocksure.db"


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_NAME,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def execute(self, query, values=()):
        self.cursor.execute(query, values)
        self.connection.commit()
        return self.cursor

    def fetchone(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetchall(self, query, values=()):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def create_tables(self):

        schema_path = os.path.join(
            os.path.dirname(__file__),
            "schema.sql"
        )

        with open(schema_path, "r", encoding="utf-8") as file:
            sql = file.read()

        self.connection.executescript(sql)
        self.connection.commit()

    def close(self):
        self.connection.close()
