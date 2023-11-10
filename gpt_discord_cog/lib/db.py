import os
import sqlite3
import datetime
from pathlib import Path

from .types import GPTConfig


def create_sqlite_db(file: os.PathLike):
    """Create a sqlite database"""
    Path(file).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE threads (
        id TEXT,
        channel_id TEXT,
        created_at INTEGER,
        PRIMARY KEY (id)
        );
        """
    )
    conn.commit()
    c.execute(
        """CREATE UNIQUE INDEX IF NOT EXISTS
        channel_id_unique_index
        ON threads (channel_id);
        """
    )
    conn.commit()
    conn.close()


def initialize_sqlite_db(file: os.PathLike):
    create_sqlite_db(file)
    return sqlite3.connect(file)


async def get_or_create_thread_from_sqlite(config: GPTConfig, channel_id: str):
    """Get or create a thread from the sqlite database"""
    conn = config["database_connection"]
    client = config["client"]
    cursor = conn.execute(
        """
         SELECT id, created_at FROM threads
         WHERE channel_id = ?
         ORDER BY created_at DESC LIMIT 1;
        """,
        (channel_id,),
    )
    row = cursor.fetchone()
    if row is None:
        thread = await client.beta.threads.create()
        conn.execute(
            """
            INSERT INTO threads (id, channel_id, created_at)
            VALUES (?, ?, ?) ;
            """,
            (thread.id, channel_id, datetime.datetime.now().timestamp()),
        )
        conn.commit()
        return thread
    thread_id, created_at = row
    if (
        created_at
        < datetime.datetime.now().timestamp() - config["conversation_lifetime"]
    ):
        # Create a new thread
        thread = await client.beta.threads.create()
        conn.execute(
            """
            INSERT INTO threads (id, channel_id, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT (id) DO UPDATE SET
            id = excluded.id,
            created_at = excluded.created_at
            ;
            """,
            (thread.id, channel_id, datetime.datetime.now().timestamp()),
        )
        conn.commit()
        return thread

    thread = await client.beta.threads.retrieve(thread_id)
    return thread
