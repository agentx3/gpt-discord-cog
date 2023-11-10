import sqlite3
from .lib.db import get_or_create_thread_from_sqlite
from .lib.types import GPTConfig


async def get_or_create_thread(channel_id: str, config: GPTConfig):
    if type(config["database_connection"]) == sqlite3.Connection:
        return await get_or_create_thread_from_sqlite(config, channel_id)
    else:
        raise NotImplementedError("Provided database is not yet supported")
