from discord import ApplicationContext
from gpt_discord_cog.lib.types import (
    CommandConfig,
    GPTConfig,
    UserGPTConfig,
)
from gpt_discord_cog.lib.utils import deep_merge_commands


def default_check(_: ApplicationContext) -> bool:
    return True


def get_default_command_config() -> CommandConfig:
    default_commands: CommandConfig = {
        "modify": {
            "name": "modify",
            "description": "Modify the assistant",
            "check": default_check,
        },
    }
    return default_commands


def merge_with_default_commands(user_config: UserGPTConfig) -> GPTConfig:
    user_commands = user_config.get("commands") or {}
    default_commands: CommandConfig = get_default_command_config()
    merged_commands: CommandConfig = deep_merge_commands(
        default_commands, user_commands
    )
    return {
        "client": user_config["client"],
        "assistant_id": user_config["assistant_id"],
        "database_connection": user_config["database_connection"],
        "database_name": user_config["database_name"],
        "conversation_lifetime": user_config["conversation_lifetime"],
        "commands": merged_commands,
    }
