import json
from gpt_discord_cog.lib.types import GPTConfig


async def generate_image_prompt(content: str, config: GPTConfig):
    client = config["client"]
    res = await client.images.generate(
        model="dall-e-3", prompt=content, size="1024x1024", quality="standard", n=1
    )
    return res.data[0].url or ""


async def parse_for_image_request(content: str, config: GPTConfig) -> tuple[str, str]:
    if not config["image"]["enable"]:
        return "", ""
    client = config["client"]
    res = await client.chat.completions.create(
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "Parse the user's Discord message to determine if it requests or suggests the need for an image. If the message indicates a desire for visual content, set 'image' to true and generate a detailed DALL-E prompt based on the message's content. Otherwise, set 'image' to false and leave the 'image_prompt' empty. Respond in JSON format: {\"image\": <boolean>, \"image_prompt\": <string>}.",
            },
            {"role": "user", "content": content},
        ],
    )
    try:
        parsed = json.loads(res.choices[0].message.content)  # type: ignore
        print(parsed)
        if parsed["image"]:
            prompt = parsed["image_prompt"]
            image_url = await generate_image_prompt(prompt, config)
            return prompt, image_url
    except Exception as e:
        print(e)
    return "", ""
