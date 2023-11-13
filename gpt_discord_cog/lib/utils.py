from typing import Any, Dict, Mapping, TypeVar

from gpt_discord_cog.lib.types import CommandConfig, UserCommandConfig

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


def deep_merge_commands(
    defaults: CommandConfig, new: UserCommandConfig
) -> CommandConfig:
    _defaults: CommandConfig = {**defaults}  # type: ignore
    for key, value in defaults.items():
        if isinstance(value, dict):
            deep_merge(value, new[key])
        elif key in new:
            print("overrriding", key)
            _defaults[key] = new[key]
    return _defaults
