from typing import Any, Dict, Mapping, TypeVar

from gpt_discord_cog.lib.types import (
    GPTConfig,
    OptionalConfig,
    UserGPTConfig,
)

T = TypeVar("T", bound=Dict[str, Any])


def deep_merge(defaults: T, new: Mapping) -> T:
    """deep_merge.
    This will mutate the defaults object with any matching keys from new

    Args:
        defaults (T): defaults
        new (Mapping): new

    Returns:
        T:
    """
    for key, value in defaults.items():
        if isinstance(value, dict):
            deep_merge(value, new[key])
        elif key in new:
            defaults[key] = new[key]
    return defaults


# Merge Function
def merge_configs(
    default_config: OptionalConfig, user_config: UserGPTConfig
) -> GPTConfig:
    # Implementation to merge configs
    # Use default_config as base and update with user_config values
    merged_config = default_config.copy()
    for key, value in user_config.items():
        if type(value) is dict:
            merged_config[key] = deep_merge(merged_config[key], value)
        elif value is not None:
            merged_config[key] = value
    return merged_config  # type: ignore
