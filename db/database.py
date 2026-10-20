"""Direct sqlite3 connection and named SQL queries (without Django ORM)."""

import sqlite3
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATABASE = ROOT / "data" / "freelance.sqlite"
QUERY_FILE = ROOT / "sql" / "queries.sql"


def connect(path=None):
    connection = sqlite3.connect(path or DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def queries():
    """Read statements introduced by -- name: ... comments."""
    result = {}
    name = None
    lines = []
    for line in QUERY_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("-- name: "):
            if name:
                result[name] = "\n".join(lines).strip()
            name = line.removeprefix("-- name: ").strip()
            lines = []
        elif name:
            lines.append(line)
    if name:
        result[name] = "\n".join(lines).strip()
    return result


def fetch(name, parameters=(), path=None):
    with closing(connect(path)) as connection:
        return connection.execute(queries()[name], parameters).fetchall()
