# GPT Discord Cog

This is a simple library meant for use with with [py-cord](https://github.com/Pycord-Development/pycord). It should also be compatible with [discord.py](https://github.com/Rapptz/discord.py).

This was made to facilitate an easy-to-implement module to add AI to your discord bot. Here are some of the details of the implementation:

* Threads are formed on a per-channel basis (Threads as defined by OpenAI, not Discord threads)
* Threads will be kept alive for some time (default 24 hours) once created. After this time period, the bot will create a new thread for the channel.
* **You must** tag the bot at the beginning of your message for it to respond
* If your message is in reply to any other message, the replied-to message will be included to the bot.
* The bot will only read its own messages, and messages that tag it at the start (in addition the contents of any message that you replied-to, even if the replied-to message did not tag the bot).


##  Installation:
Since I don't have this on pypi yet, you can put this in your requirements.txt 

`gpt_discord_cog@git+https://github.com/agentx3/gpt-discord-cog@master`

or if you're using poetry put this in your dependencies:

`gpt_discord_cog = { git = "https://github.com/agentx3/gpt-discord-cog.git"} ` 

## Usage:

You will first need to create an Assistant and get its ID via OpenAIs API. See their [documentation](https://platform.openai.com/docs/api-reference/assistants). 

```python
from gpt_discord_cog import LiveGPTConversation, initialize_sqlite_db
from openai import AsyncOpenAI


# Initialize your bot ...


client = AsyncOpenAI(...)
db_name = "gpt-conversations.db" # The sqlite file name

# Pass in a Pathlike object to the target sqlite file, it will be created if it doesn't exist
conn = initialize_sqlite_db(Path(os.getcwd()) / "gpt-conversations" / db_name)

bot.add_cog(
    LiveGPTConversation(
        bot,
        {
            "client": client,
            "assistant_id": ASSISTANT_ID,
            "database_name": db_name,
            "database_connection": conn,
            "conversation_lifetime": 60 * 60 * 24, # Number in seconds for a thread to live once created
        },
    )
)

# ...

bot.run("YourBotToken")

```

