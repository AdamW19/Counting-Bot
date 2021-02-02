"""
The main runner of Counting Bot, a bot that counts up and up and up.
Theoretically the bot will not stop counting up due to Python's unbounded integer boundary.

Sources: Would like to thank ktraw2's TVBot for the error printing and discord.py's documentation
"""
import config
from discord.ext import commands

EXTENSIONS = ["cogs.counting"]

"""
The body of Counting Bot. Executes the Discord client and the main bot code.
"""


class CountingBot(commands.Bot):
    """
    Constructor for Counting Bot. Sets up the bot and its extensions
    """

    def __init__(self, extensions):
        super().__init__(command_prefix=config.prefix, description=config.description, case_insensitive=True)

        for e in extensions:
            self.load_extension(e)

    async def on_ready(self):
        print("Ready")


CountingBot(EXTENSIONS).run(config.token)
