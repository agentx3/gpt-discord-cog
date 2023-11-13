from discord import ApplicationContext
from gpt_discord_cog.lib.types import (
    ImageConfig,
    OptionalConfig,
)


def default_check(_: ApplicationContext) -> bool:
    return True


def get_default_config():
    default_config: OptionalConfig = {
        "commands": {
            "modify": {
                "name": "modify",
                "description": "Modify the assistant",
                "check": default_check,
            },
        },
        "image": {"enable": False},
    }
    return default_config


def get_default_image_config() -> ImageConfig:
    default_image: ImageConfig = {"enable": False}
    return default_image
