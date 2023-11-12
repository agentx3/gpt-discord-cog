import asyncio
from typing import Callable
import discord

from discord.ext import commands
from .conversation import handle_message
from .lib.types import GPTConfig, UserGPTConfig
from .lib.defaults import merge_with_default_commands
from .assistants import modify_assistant
from functools import wraps


def check_for(check_func: Callable[[discord.ApplicationContext], bool]):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: discord.ApplicationContext):
            if check_func(ctx):
                await func(self, ctx)
            else:
                await ctx.respond(
                    "You are not authorized to use this command", ephemeral=True
                )

        return wrapper

    return decorator


def create_cog(
    bot: commands.Bot, user_config: UserGPTConfig, *args, **kwargs
) -> commands.Cog:
    """create_cog.
    Kwargs should be arguments accepted by the CogMeta metaclass

    Args:
        bot (commands.Bot): bot
        config (GPTConfig): config
        args:
        kwargs:

    Returns:
        commands.Cog:
    """

    # Merge the default commands with the user's commands
    config = merge_with_default_commands(user_config)

    # Defining a class inside a function is a bit icky, but we're doing this
    # to directly pass kwargs to the metaclass constructor, a necessity given that
    # several of our desired properties are class-level, not instance-level.
    # This approach, while a bit unorthodox, is our best bet for the dynamic
    # customization needed in this scenario.
    class LiveGPTConversation(
        commands.Cog,
        *args,
        **kwargs,
    ):
        def __init__(self, bot: commands.Bot, config: GPTConfig):
            self.bot = bot
            self.openai_client = config["client"]
            self.config = config
            self.message_queue = asyncio.Queue()
            # Start the task to process messages
            self.bot.loop.create_task(self.process_messages())

        async def process_messages(self):
            while True:
                try:
                    msg = await self.message_queue.get()
                    await handle_message(msg, self.bot, self.config)
                    self.message_queue.task_done()
                except asyncio.CancelledError:
                    return
                except Exception as e:
                    print(e)

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

        @discord.slash_command(
            name=config["commands"]["modify"]["name"],
            description=config["commands"]["modify"]["description"],
        )
        @check_for(config["commands"]["modify"]["check"])
        async def modify(self, ctx: discord.ApplicationContext):
            await modify_assistant(ctx, self.config)

    return LiveGPTConversation(bot, config)
