Moderation Bot -----------------------------------

This is a Discord bot with HEAVY moderation features.

Getting Started ---------------------------

1. Clone this repository

2. Create a virtual environment with python -m venv env

3. Activate the virtual environment with env\Scripts\activate (Windows) or source env/bin/activate (Linux/macOS)

4. Install the required packages with pip install -r requirements.txt

Creating a new .env file ------------------

Create a .env file in the root directory of the project with the following environment variables:

DISCORD_TOKEN=<your_bot_token>
DISCORD_GUILD=<your_guild_name>

Run the bot with python bot.py

Commands ---------------------------------

/help - displays all the available commands
/ban - bans a member of the discord
/kick - Kicks a member from the discord
/unban - Unbans a member that was banned
/purge - Delete a specified number of messages
/whitelist - remove or add words to the whitelist
/mute - mute a specific member in discord
/unmute - unmute a specific member in discord
/list_banned - List all profanity words
/list_whitelisted - List all whitelisted words

Credits --------------------------------

This bot was created by [4EyesMarcus].
