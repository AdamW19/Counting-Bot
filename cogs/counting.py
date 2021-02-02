"""
The main code of Counting Bot, a bot that counts up and up and up.
Theoretically the bot will not stop counting up due to Python's unbounded integer boundary.

Source: discord.py's documentation
"""
import time
import config
from discord.ext import commands

# Which arg to parse for start command
STARTING_NUM_ARG = 0
ENDING_NUM_ARG = 1

SENTINEL_VAL = STARTING_NUM_ARG - 1

# The default value to start from if not given in start()
DEFAULT_VAL = config.default_starting_value

# The amount of seconds to wait before incrementing
TIME_PER_COUNT = config.default_time_between_count

"""
The main code of Counting Bot, a bot that counts up and up and up.
"""


class Counting(commands.Cog):
    """
    Constructor for Counting.

    Class variables:
    bot -- the bot Discord instance
    current_num -- The current number the bot is on
    is_running -- True if the bot is counting, false otherwise
    """
    def __init__(self, bot):
        self.bot = bot
        self.current_num = 0
        self.is_running = False

    """
    Helper function that counts up from a given point or from a previous point.
    
    Prints out to the channel the original command was executed on.
    """
    async def count_up(self, ctx):
        count = self.current_num
        while self.is_running:
            await ctx.send(str(count))
            time.sleep(TIME_PER_COUNT)
            count = count + 1
            self.current_num = count

    """
    The "start" command. Starts the counting sequence. Requires the "manage messages" role to run.
    
    Prints to the channel the command was executed on via count_up().
    
    """
    @commands.group(case_insensitive=True, invoke_without_command=True, aliases=["s", "initialize", "init"])
    @commands.has_permissions(manage_messages=True)
    async def start(self, ctx, *args):
        starting_val = DEFAULT_VAL  # default value

        # If a command has already started, prints error to kill before continuing
        if self.is_running:
            await ctx.send(":warning: Unable to start! Bot is already counting, use command `-stop` to stop counting")
            return

        # Checks to see if an argument was provided
        if len(args) <= 0:
            # If not, go with default value
            await ctx.send(":warning: No starting number given, defaulting to {}...".format(DEFAULT_VAL))
        # Otherwise try to parse it as an int and set it as the starting val
        else:
            try:
                starting_val = int(args[STARTING_NUM_ARG])
            # Error if argument is invalid
            except ValueError:
                await ctx.send(":warning: You have an invalid starting value, defaulting to {}...".format(DEFAULT_VAL))

        # Sets count_up up and runs it
        self.current_num = starting_val
        self.is_running = True
        await ctx.send("Starting count...")
        await Counting.count_up(self, ctx)

    """
    The "stop" command. Stops the bot from counting if needed. Requires the "manage messages" role to run.
    
    Prints to the channel the command was executed on.
    """
    @commands.group(case_insensitive=True, invoke_without_command=True, aliases=["end", "e", "terminate", "kill"])
    @commands.has_permissions(manage_messages=True)
    async def stop(self, ctx):
        # kills loop in count_up()
        self.is_running = False
        await ctx.send("Stopping count... ")

    """
    The "continue" command. Continues the bot by parsing previous bot output to get the previous count.
    """
    @commands.group(case_insensitive=True, invoke_without_command=True, aliases=["continue", "c"])
    @commands.has_permissions(manage_messages=True)
    async def cont(self, ctx):
        # -1 to indicate that value hasn't changed
        continue_val = SENTINEL_VAL

        # Parses the current channel, and looks for the last message the bot was sent while counting
        channel = ctx.channel
        messages = await channel.history().flatten()

        # Gets the value from message
        for mess in messages:
            if mess.author.id != self.bot.user.id:  # checks if the message we're checking is itself
                continue
            else:
                try:
                    continue_val = int(mess.content)  # converting str to int, if it fails it's not a counting message
                except ValueError:
                    continue
                else:
                    break

        # if the value is unchanged, then the last bot command could not be found
        if continue_val == SENTINEL_VAL:
            await ctx.send(":warning: Unable to get last bot message")
            return

        # Sets up count_up
        self.is_running = True
        self.current_num = continue_val + 1  # +1 cause we got the last number the bot was on
        await ctx.send("Continuing from last time...")
        await Counting.count_up(self, ctx)


def setup(bot):
    bot.add_cog(Counting(bot))
