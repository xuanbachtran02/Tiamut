from __future__ import annotations
from sqlite3 import connect

import datetime as dt
import logging
import os
import re
import typing as t
from pathlib import Path

log = logging.getLogger(__name__)


class Database():
    __slots__ = ("db_path", "sql_path", "calls", "db", "cur")

    def __init__(self, db_path, build_path) -> None:
        self.db_path = db_path
        self.sql_path = build_path
        self.calls = 0

    def connect(self) -> None:
        self.db = connect(self.db_path, check_same_thread=False)
        self.cur = self.db.cursor()
        log.info(f"Connected to database at {self.db_path}")

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()
        log.info("Closed database connection")

    def execute(self, command, *values):
        self.cur.execute(command, tuple(values))

    def scriptexec(self, path):
        with open(path, 'r', encoding="utf-8") as script:
            self.cur.executescript(script.read())


if __name__ == "__main__":
    DB_PATH = "./database/test.db"
    BUILD_PATH = "./schema/schema.sql"
    db = Database(DB_PATH, BUILD_PATH)
    db.connect()
