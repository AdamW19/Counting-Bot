"""
The main runner of Counting Bot, a bot that counts up and up and up.
Theoretically the bot will not stop counting up due to Python's unbounded integer boundary.

Sources: Would like to thank ktraw2's TVBot for the error printing and discord.py's documantation
"""
import config
import discord
import traceback
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

    """
    Runs when a command has been successfully parsed. Prints into a logging channel for logging purposes
    """
    async def on_command(self, ctx):
        await self.wait_until_ready()
        await self.get_channel(config.logger_channel_id).send("Command received from `" + ctx.author.name + "` on `" +
                                                             ctx.guild.name + "`: " + "`" + ctx.message.content + "`")

    """
    Runs when a command gives an error. Parses and prints out error to user.
    """
    async def on_command_error(self, ctx, error):
        # HTTP error
        if isinstance(error, discord.HTTPException) and not hasattr("on_error", ctx.command):
            await self.send_unexpected_error(ctx, error)
        # Invalid command
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send(":x: Sorry, `" + ctx.invoked_with +
                               "` is not a valid command.  Type `s!help` for a list of commands.")
            await self.get_channel(config.logger_channel_id).send("Invalid command received from `" + ctx.author.name +
                                                                 "` on `" + ctx.guild.name + "`: " +
                                                                 ctx.message.content)
        # Permissions error
        elif isinstance(error, discord.ext.commands.CheckFailure):
            # Generic error command
            if ctx.invoked_with == "form":
                await ctx.send(":warning: You are not authorized to run this command.")
            # Required permissions to use bot
            else:
                await ctx.send(":warning: You are not authorized to run this command, "
                                   "to be able to run `" + ctx.invoked_with +
                                   "` you must have the `Manage Messages` permission.")
        # Bad argument error
        elif isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send(":x: Your command arguments could not be interpreted, please try again (Did you forget a"
                           " \" character?).")
            await self.get_channel(config.logger_channel_id).send("Invalid command arguments received from `" +
                                                                 ctx.author.name + "` on `" + ctx.guild.name + "`: " +
                                                                 ctx.message.content)
        # Everything else
        else:
            await self.send_unexpected_error(ctx, error)

    """
    Runs when a run-time error occurs that is most likely due to buggy code.
    
    Logs error into the logger channel.
    """
    async def send_unexpected_error(self, ctx, error):
        await ctx.send(":warning: An unexpected error occurred and a report has been sent to the developer.")
        tb = traceback.extract_tb(tb=error.original.__traceback__)
        await self.get_channel(config.logger_channel_id).send(":warning: An unexpected error occurred of type `" +
                                                             type(error).__name__ + "` for message `" +
                                                             ctx.message.content + "`: `" + str(error) + "`" +
                                                             " in function `" + tb[-1].name + "`" +
                                                             " on line `" + str(tb[-1].lineno) + "`" +
                                                             " in file `" + tb[-1].filename + "`")


CountingBot(EXTENSIONS).run(config.token)
