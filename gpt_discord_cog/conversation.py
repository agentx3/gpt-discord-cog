import asyncio

import discord
from discord.ext.commands import Bot
from openai.types.beta.threads import MessageContentText

from .lib.types import GPTConfig
from .threads import get_or_create_thread


async def handle_message(msg: discord.Message, bot: Bot, config: GPTConfig):
    # Check that the first thing is that it mentions the bot
    assert bot.user
    if not msg.content.startswith(f"<@{bot.user.id}>"):
        return
    # Don't respond to bots
    if msg.author.bot:
        return
    # Should be in a public channel
    if type(msg.channel) not in [discord.Thread, discord.TextChannel]:
        return
    thread = await get_or_create_thread(str(msg.channel.id), config)
    client = config["client"]
    assistant_id = config["assistant_id"]
    content = (
        msg.author.display_name
        + ":"
        + msg.content.replace(f"<@{bot.user.id}>", "", 1).replace(
            f"<@!{bot.user.id}>", bot.user.display_name
        )
    )
    if ref := msg.reference:
        if type(ref.resolved) == discord.Message:
            content += f"""
<{{This message was a reply to the following message:
<START OF REFERENCED MESSAGE>
{ref.resolved.author.display_name}: {ref.resolved.content}
<END OF REFERENCED MESSAGE>
}}>
"""

    try:
        await client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=content
        )
        run = await client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        async with msg.channel.typing():
            while run.status == "in_progress" or run.status == "queued":
                await asyncio.sleep(1)
                run = await client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id,
                )
        if run.status == "completed":
            messages = await client.beta.threads.messages.list(thread_id=thread.id)
            response = list(
                filter(lambda t: t.type == "text", messages.data[0].content)
            )[0]
            assert type(response) == MessageContentText
            response_text = response.text.value
            await msg.reply(response_text)
            return
    except Exception as e:
        await msg.reply(f"Error: {e}")
    return
