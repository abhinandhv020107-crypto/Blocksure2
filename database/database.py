"""SQLite database helper for BlockSure."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Optional

DATABASE_PATH = Path(__file__).resolve().parent.parent / "blocksure.db"

class Database:
    def __init__(self, database_path: Optional[str | Path] = None) -> None:
        self.database_path = Path(database_path) if database_path else DATABASE_PATH
        self.connection = sqlite3.connect(self.database_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")

    def execute(self, query: str, values: Iterable[Any] = ()) -> sqlite3.Cursor:
        cursor = self.connection.execute(query, tuple(values))
        self.connection.commit()
        return cursor

    def fetchone(self, query: str, values: Iterable[Any] = ()):
        return self.connection.execute(query, tuple(values)).fetchone()

    def fetchall(self, query: str, values: Iterable[Any] = ()):
        return self.connection.execute(query, tuple(values)).fetchall()

    def create_tables(self) -> None:
        schema_path = Path(__file__).resolve().parent / "schema.sql"
        self.connection.executescript(schema_path.read_text(encoding="utf-8"))
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
