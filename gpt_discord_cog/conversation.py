import asyncio

import discord
from discord.ext.commands import Bot
from openai.types.beta.threads import MessageContentText

from .image import parse_for_image_request

from .lib.types import GPTConfig
from .threads import get_or_create_thread


async def get_text_response(content: str, thread_id: str, config: GPTConfig):
    client = config["client"]
    assistant_id = config["assistant_id"]
    try:
        await client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=content
        )
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        while run.status == "in_progress" or run.status == "queued":
            await asyncio.sleep(1)
            run = await client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
        if run.status == "completed":
            messages = await client.beta.threads.messages.list(thread_id=thread_id)
            response = list(
                filter(lambda t: t.type == "text", messages.data[0].content)
            )[0]
            assert type(response) == MessageContentText
            response_text = response.text.value
            return response_text
        else:
            raise Exception("Run failed")
    except Exception as e:
        return f"Error: {e}"


async def handle_message(msg: discord.Message, bot: Bot, config: GPTConfig):
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

    async with msg.channel.typing():
        response_text, response_image_prompt_and_url = await asyncio.gather(
            get_text_response(content, thread.id, config),
            parse_for_image_request(content, config),
        )
    prompt, image_url = response_image_prompt_and_url
    if not image_url:
        await msg.reply(response_text)
        return
    embed = discord.Embed(title="Image", description=prompt)
    embed.set_image(url=image_url)
    # Download the image and convert to a discord.File
    await msg.reply(content=response_text, embed=embed)
    return
