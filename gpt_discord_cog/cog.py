import asyncio
from typing import List
import discord

from discord.ext import commands
from .conversation import handle_message
from .lib.types import GPTConfig


class LiveGPTConversation(commands.Cog):
    def __init__(self, bot: commands.Bot, config: GPTConfig):
        self.bot = bot
        self.openai_client = config["client"]
        self.config = config
        self.message_queue = asyncio.Queue()
        # Start the task to process messages
        self.bot.loop.create_task(self.process_messages())

    async def process_messages(self):
        while True:
            msg = await self.message_queue.get()
            await handle_message(msg, self.bot, self.config)
            self.message_queue.task_done()

    @commands.Cog.listener("on_message")
    async def on_message(self, msg: discord.Message):
        assert self.bot.user
        if not msg.content.startswith(f"<@{self.bot.user.id}>"):
            return
        # Don't respond to bots
        if msg.author.bot:
            return
        # Should be in a public channel
        if type(msg.channel) not in [discord.Thread, discord.TextChannel]:
            return

        await self.message_queue.put(msg)
