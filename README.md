JoJo Moderation bot is a Discord bot that automatically detects and handles messages containing profanity. It keeps track of user offenses and applies timeouts or bans based on the number of offenses. Mainly used for streamer/youtube communities.

Features:

Automatic detection of profanity in messages
Keeps track of user offenses and applies timeouts or bans based on the number of offenses
Whitelist system for words that shouldn't trigger offenses
Mute role integration for timeouts
Ability to reset warnings for a specified member
Ticket system for users to request support and get their issues resolved by staff
Setup:

Clone the repository
Install the required packages using pip install -r requirements.txt
Create a bot on the Discord Developer Portal and obtain its token
Add the bot to your server using the invite link generated in the Developer Portal
Edit the config.json file with your bot token and desired settings
Run python bot.py to start the bot

Usage:

The bot will automatically detect and handle messages containing profanity. Offenses are tracked and timeouts or bans are applied based on the number of offenses.
To reset warnings for a specified member, use the /resetwarnings command. By default, the command resets warnings for the command user.
To open a support ticket, use the /ticket command. Staff can close tickets using the /close command.
Code:

The main code for the bot is in bot.py.
The check_message function checks each message for profanity and handles it appropriately.
The resetwarnings function is a slash command that resets warnings for a specified member.
The Ticket class in tickets.py handles the ticket system and includes methods for opening and closing tickets.
