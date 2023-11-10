import discord

from discord.ext import commands
from .conversation import handle_message
from .lib.types import GPTConfig


class LiveGPTConversation(commands.Cog):
    def __init__(self, bot: commands.Bot, config: GPTConfig):
        self.bot = bot
        self.openai_client = config["client"]
        self.config = config

    @commands.Cog.listener("on_message")
    async def on_message(self, msg: discord.Message):
        await handle_message(msg, self.bot, self.config)
