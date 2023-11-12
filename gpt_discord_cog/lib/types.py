from typing import (
    Callable,
    Optional,
    TypedDict,
)
from discord import ApplicationContext

from openai import AsyncOpenAI
import sqlite3


class UserCommandOptions(TypedDict, total=False):
    # This should be compatible with the rules for a discord command name
    name: Optional[str]
    description: Optional[str]
    check: Callable[[ApplicationContext], bool]


class UserCommandConfig(TypedDict, total=False):
    modify: UserCommandOptions


class CommandOptions(TypedDict):
    # This should be compatible with the rules for a discord command name
    name: str
    description: str
    check: Callable[[ApplicationContext], bool]


class CommandConfig(TypedDict):
    modify: CommandOptions


class UserGPTConfig(TypedDict):
    """The only purpose for this is to make some of the keys optional"""

    client: AsyncOpenAI
    assistant_id: str
    database_connection: sqlite3.Connection  # TODO: Add a handler for redis
    database_name: str
    conversation_lifetime: int
    commands: Optional[UserCommandConfig]


class GPTConfig(TypedDict):
    client: AsyncOpenAI
    assistant_id: str
    database_connection: sqlite3.Connection  # TODO: Add a handler for redis
    database_name: str
    conversation_lifetime: int
    commands: CommandConfig
