# Counting-Bot
A Discord bot that counts to infinity. This bot counts up from a number until the bot dies, the channel is deleted, or until the heat death of the universe due to [Python 3 integers being unbounded](https://www.tutorialspoint.com/what-is-the-maximum-possible-value-of-an-integer-in-python).

# Commands

The bot has 3 commands. All of these commands must be run by someone with the "Manages Messages" role. 

- `start`
  - Starts the counting in the channel you are in. You may give it an initial starting point: `-start 69` if you so wish. The default starting value is 0.
  - You may also use `s`, `initialize`, or `init` to run this command.
- `end`
  - End the counting. Will stop counting immediately upon command execution.
  - You may also use `e`, `terminate`, `kill`, or `stop` to run this command.
- `continue`
  - Continues the counting by parsing the last message the bot posted while the bot was still counting. Will give you an error if the bot could not find a previous message.
  - You may also use `cont` or `c` to run this command.

# How to run
After cloning the repository and downloading [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html#installing), rename `config_public.py` to `config.py` and add your private Discord bot token, 
the bot's user id, and a channel id for logging. After that, run `python3 Counting Bot.py`.

You may need to run it as `python3 Counting\ Bot.py`,

# Bugs
If you notice any bugs, please make a ticket under the Issues tab. Or if you're super great, write your own fix and make a pull request. Please note that this bot was initially writen -- from start to finish -- in roughly 4 hours.

# Sources
I used to use run-time command and error parsing from ktraw2's [TVBot](https://github.com/ktraw2/TVBot). I also used [discord.py's documentation](https://discordpy.readthedocs.io/en/latest/), but I don't anymore.

Regardless, thank you for the error/command parsing!

# License
Per ktraw2's [TVBot](https://github.com/ktraw2/TVBot) license, Counting Bot is under the GNU General Public License v3.0. Please view the license [here](./LICENSE).
