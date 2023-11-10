from typing import (
    TypedDict,
)

from openai import AsyncOpenAI
from openai.types.beta import Assistant, Thread
import sqlite3


class GPTConfig(TypedDict):
    client: AsyncOpenAI
    assistant_id: str
    database_connection: sqlite3.Connection  # TODO: Add a handler for redis
    database_name: str
    conversation_lifetime: int
