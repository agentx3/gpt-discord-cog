from setuptools import setup, find_packages

if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    setup(
        # Needed to silence warnings (and to be a worthwhile package)
        name="gpt_discord_cog",
        url="https://github.com/agentx3/gpt-discord-cog",
        author="Agent X3",
        author_email="thepuzzlegang.agent@gmail.com",
        # Needed to actually package something
        packages=find_packages(),
        version="1.31",
        description="A cog for py-cord that easily attaches an OpenAI assisatnt to a bot",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=["openai", "py-cord"],
        python_requires=">=3.10",
        classifiers=[
            "Programming Language :: Python :: 3.10",
            "Operating System :: OS Independent",
        ],
    )
