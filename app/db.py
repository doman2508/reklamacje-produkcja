"""Database helpers for the reklamacje (claims) app."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Optional

# Path to the SQLite database file (relative to project root).
DB_PATH = os.path.join("data", "reklamacje.db")


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection and ensure the database/tables exist."""
    # Make sure the data directory exists before connecting.
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    # Ensure foreign keys are enforced (good practice with SQLite).
    connection.execute("PRAGMA foreign_keys = ON;")

    # Create tables on first run (idempotent).
    create_tables(connection)
    return connection


def create_tables(connection: sqlite3.Connection) -> None:
    """Create the reklamacje table if it does not already exist."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS reklamacje (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_zgloszenia TEXT NOT NULL,
            tytul_zgloszenia TEXT NOT NULL,
            opis TEXT,
            ilosc INTEGER NOT NULL CHECK (ilosc > 0),
            status TEXT NOT NULL,
            utworzono TEXT NOT NULL,
            zglaszajacy TEXT,
            kod_wyrobu TEXT,
            nazwa_wyrobu TEXT,
            kkw TEXT,
            claim_number TEXT UNIQUE
        );
        """
    )
    connection.commit()


def add_reklamacja(
    data_zgloszenia: str,
    tytul_zgloszenia: str,
    opis: Optional[str],
    ilosc: int,
    zglaszajacy: Optional[str] = None,
    kod_wyrobu: Optional[str] = None,
    nazwa_wyrobu: Optional[str] = None,
    kkw: Optional[str] = None,
    claim_number: Optional[str] = None,
    status: str = "NOWE",
) -> int:
    """Insert a new reklamacja row and return its id."""
    # Automatically set the creation timestamp.
    utworzono = datetime.now().isoformat(sep=" ", timespec="seconds")

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO reklamacje (
                data_zgloszenia,
                tytul_zgloszenia,
                opis,
                ilosc,
                status,
                utworzono,
                zglaszajacy,
                kod_wyrobu,
                nazwa_wyrobu,
                kkw,
                claim_number
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                data_zgloszenia,
                tytul_zgloszenia,
                opis,
                ilosc,
                status,
                utworzono,
                zglaszajacy,
                kod_wyrobu,
                nazwa_wyrobu,
                kkw,
                claim_number,
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)
    
def list_reklamacje():
    """
    Returns all nonconformance claims from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            data_zgloszenia,
            tytul_zgloszenia,
            ilosc,
            status,
            zglaszajacy,
            claim_number
        FROM reklamacje
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows

    
    
if __name__ == "__main__":
    # Initialize database and create tables on direct run
    conn = get_connection()
    conn.close()
    print("Baza SQLite została utworzona.")


