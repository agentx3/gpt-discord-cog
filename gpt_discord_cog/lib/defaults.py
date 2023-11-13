from discord import ApplicationContext
from gpt_discord_cog.lib.types import (
    CommandConfig,
    GPTConfig,
    ImageConfig,
    UserGPTConfig,
)
from gpt_discord_cog.lib.utils import deep_merge, deep_merge_commands


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


def get_default_image_config() -> ImageConfig:
    default_image: ImageConfig = {"enable": False}
    return default_image


def merge_with_default_commands(user_config: UserGPTConfig) -> GPTConfig:
    user_commands = user_config.get("commands") or {}
    default_commands: CommandConfig = get_default_command_config()
    merged_commands: CommandConfig = deep_merge_commands(
        default_commands, user_commands
    )
    user_image_config = user_config.get("image") or {}
    default_image: ImageConfig = get_default_image_config()
    merged_image: ImageConfig = deep_merge(default_image, user_image_config)  # type: ignore

    return {
        "client": user_config["client"],
        "assistant_id": user_config["assistant_id"],
        "database_connection": user_config["database_connection"],
        "database_name": user_config["database_name"],
        "conversation_lifetime": user_config["conversation_lifetime"],
        "commands": merged_commands,
        "image": merged_image,
    }
