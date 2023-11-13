from typing import Type, TypedDict
import unittest
from unittest.mock import Mock, create_autospec
from openai import AsyncOpenAI
from gpt_discord_cog.lib.types import OptionalConfig, UserGPTConfig, GPTConfig
from gpt_discord_cog.lib.defaults import get_default_config
from sqlite3 import Connection

from gpt_discord_cog.lib.utils import merge_configs
from tests.utils import assert_dict_structure


class TestConfig(unittest.TestCase):
    """
    Test the config merging functionality to ensure that the default config is merged with the user config
    and results in the full GPTConfig object.
    """

    def setUp(self):
        # Create a mock object
        self.mock_connection: Connection = create_autospec(Connection)
        self.mock_client: AsyncOpenAI = create_autospec(AsyncOpenAI)

    def test_all_provided(self):
        # Use the mock object in your tests
        default_config = get_default_config()
        custom_description = "Modify the assistant!!!"
        user_config: UserGPTConfig = {
            "client": self.mock_client,
            "assistant_id": "assistant_id",
            "database_name": "database_name",
            "database_connection": self.mock_connection,
            "conversation_lifetime": 60 * 60 * 24,
            "commands": {
                "modify": {"check": lambda ctx: True, "description": custom_description}
            },
            "image": {
                "enable": True,
            },
        }
        # Perform the merge
        merged_config = merge_configs(default_config, user_config)
        unittest.TestCase().assertEqual(
            merged_config["commands"]["modify"]["description"], custom_description
        )

        assert_dict_structure(self, dict(merged_config), GPTConfig)

    def test_some_provided(self):
        default_config = get_default_config()
        user_config: UserGPTConfig = {
            "client": self.mock_client,
            "assistant_id": "assistant_id",
            "database_name": "database_name",
            "database_connection": self.mock_connection,
            "conversation_lifetime": 60 * 60 * 24,
            "image": {
                "enable": True,
            },
        }
        # Perform the merge
        merged_config = merge_configs(default_config, user_config)
        unittest.TestCase().assertEqual(merged_config["image"]["enable"], True)

        assert_dict_structure(self, dict(merged_config), GPTConfig)

    def test_some_provided_2(self):
        # Use the mock object in your tests
        default_config = get_default_config()
        user_config: UserGPTConfig = {
            "client": self.mock_client,
            "assistant_id": "assistant_id",
            "database_name": "database_name",
            "database_connection": self.mock_connection,
            "conversation_lifetime": 60 * 60 * 24,
            "commands": {
                "modify": {
                    "description": "Modify the assistant!!!",
                }
            },
        }
        # Perform the merge
        merged_config = merge_configs(default_config, user_config)

        assert_dict_structure(self, dict(merged_config), GPTConfig)


# Run the test
if __name__ == "__main__":
    unittest.main()
