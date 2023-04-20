from asyncio import Event
import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands
import os
import json
import time
import asyncio

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = {}

        self.profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        self.whitelist_file_path = os.path.join(os.path.dirname(__file__), 'whitelist.json')
        self.warnings_file_path = os.path.join(os.path.dirname(__file__), 'user_warnings.json')
        self.settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')

# Loading Data Files
        try:
            with open(self.profanity_file_path, 'r') as f:
                self.profanity = f.read().splitlines()
        except FileNotFoundError:
            print("File not found: profanity.txt")
            self.profanity = []
        try:
            with open(self.whitelist_file_path, 'r') as f:
                self.whitelist = json.load(f)
        except FileNotFoundError:
            print("File not found: whitelist.json")
            self.whitelist = {}
        try:
            with open(self.warnings_file_path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}
#Defines settings        
    def get_settings():
        with open("settings.json", "r") as f:
            settings = json.load(f)
        return settings

    def save_settings(settings):
        with open("settings.json", "w") as f:
            json.dump(settings, f)

#Moderation Commands

    @slash_command(name="whitelist", description="Add or remove a word from the whitelist")
    async def whitelist(self, ctx: Interaction, action: str = None, word: str = None):
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You do not have the required permissions to use this command.")
            return

        if action not in ["add", "remove"]:
            await ctx.send("Invalid action. Please specify 'add' or 'remove' as the first argument.")
            return

        if not word:
            await ctx.send("Please specify a word to whitelist.")
            return

        whitelist_file_path = os.path.join(os.getcwd(), "whitelist.json")  # use a single file for all guilds

        try:
            with open(whitelist_file_path, 'r') as f:
                self.whitelist = json.load(f)
        except FileNotFoundError:
            self.whitelist = {}

        guild_id = str(ctx.guild.id)
        if guild_id not in self.whitelist:
            self.whitelist[guild_id] = {}

        if action == "add":
            if word in self.whitelist[guild_id] and self.whitelist[guild_id][word]:
                await ctx.send(f"{word} is already whitelisted.")
                return
            if word in self.profanity and word not in self.whitelist[guild_id]:
                self.profanity.remove(word)
                with open(self.profanity_file_path, 'w') as f:
                    f.write('\n'.join(self.profanity))
            self.whitelist[guild_id][word] = True
            with open(whitelist_file_path, 'w') as f:
                json.dump(self.whitelist, f)
            await ctx.send(f"{word} has been added to the whitelist.")
        elif action == "remove":
            if word not in self.whitelist[guild_id]:
                await ctx.send(f"{word} is not currently whitelisted.")
                return
            del self.whitelist[guild_id][word]
            with open(whitelist_file_path, 'w') as f:
                json.dump(self.whitelist, f)
            with open(self.profanity_file_path, 'a') as f:
                f.write('\n' + word)
            await ctx.send(f"{word} has been removed from the whitelist.")


    @slash_command(name="ban", description="Ban a member of this discord")
    async def ban(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
        reason: str = nextcord.SlashOption(name='reason', description='Please provide a reason')
    ):
        
        if not ctx.user.guild_permissions.ban_members:
            await ctx.send("You do not have the required permissions to use this command.")
            return
    
        if not reason: reason = "No reason"
        await member.ban(reason=reason)
        await ctx.response.send_message(f"{member} has been banned by {ctx.user.mention} for {reason}")
        
        
    @slash_command(name="unban", description="Unban a member of this discord")
    async def unban(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
    ):
        if not ctx.user.guild_permissions.ban_members:
            await ctx.send("You do not have the required permissions to use this command.")
        await ctx.guild.unban(user=member)
        await ctx.response.send_message(f"{member} has been unbanned")


    @slash_command(name="kick", description="Kick a member of this discord")
    async def kick(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
):
        if not ctx.user.guild_permissions.kick_members:
            await ctx.response.send_message("You do not have the required permissions to use this command.")
        else:
            await ctx.guild.kick(user=member)
            await ctx.response.send_message(f"{member} has been kicked")



    @slash_command(name="mute", description="Mute Member in text chat")
    async def mute(self, ctx: Interaction, member: nextcord.Member, reason: str):
        if not ctx.user.guild_permissions.mute_members:
            await ctx.send("You do not have the required permissions to use this command.")
        else:
            muted_role = nextcord.utils.get(ctx.guild.roles, name="muted")
            await member.add_roles(muted_role)
            await ctx.send(f"{member.mention} has been muted because {reason}")
        
        
        
    @slash_command(name="unmute", description="Unmute a member in discord")
    async def unmute(self, ctx:Interaction, member:nextcord.Member):
        if not ctx.user.guild_permissions.mute_members:
            await ctx.send("You do not have the required permissions to use this command.")
        else:
            muted_role = nextcord.utils.get(ctx.guild.roles, name="muted")
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} has been unmuted.")
        

    @slash_command(name="purge", description="Delete a specified number of messages")
    async def purge(self, interaction: nextcord.Interaction, limit: int):
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.response.send_message("You do not have permission to delete messages.", ephemeral=True)
            return
        await interaction.channel.purge(limit=limit + 1)
        await interaction.response.send_message(f"Deleted {limit} messages.", ephemeral=True)

    @slash_command(name="list_banned", description="Lists all profanity words.")
    async def list_banned(self, ctx: Interaction):
    # Get the full path to the profanity file
        profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')

    # Open the profanity file and read its contents
        with open(profanity_file_path, "r") as profanity_file:
            profanity_words = [line.strip() for line in profanity_file]

    # Split the profanity words into chunks of 50 to avoid exceeding the character limit
        profanity_word_chunks = [profanity_words[i:i+50] for i in range(0, len(profanity_words), 50)]

    # Create an embed for each chunk of profanity words
        for i, chunk in enumerate(profanity_word_chunks):
            words_embed = nextcord.Embed(title="List of Profanity Words")
            words_embed.add_field(name=f"Profanity Words (part {i+1})", value="\n".join(chunk), inline=False)

        # Truncate any fields that are longer than 1024 characters
            for field in words_embed.fields:
                if len(field.value) > 1024:
                    field.value = field.value[:1021] + "..."
        
            await ctx.send(embed=words_embed)

    @slash_command(name="list_whitelisted", description="Lists all whitelisted words.")
    async def list_whitelisted(self, ctx: Interaction):
    # Get the full path to the whitelist file
        whitelist_file_path = os.path.join(os.path.dirname(__file__), 'whitelist.json')

    # Open the whitelist file and read its contents
        with open(whitelist_file_path, "r") as whitelist_file:
            whitelist_words = json.load(whitelist_file)

    # Convert any frozensets to strings
        whitelist_words = [str(word) for word in whitelist_words]

    # Split the whitelist words into chunks of 50 to avoid exceeding the character limit
        whitelist_word_chunks = [whitelist_words[i:i+50] for i in range(0, len(whitelist_words), 50)]

    # Create an embed for each chunk of whitelist words
        for i, chunk in enumerate(whitelist_word_chunks):
            words_embed = nextcord.Embed(title="List of Whitelisted Words")
            words_embed.add_field(name=f"Whitelist Words (part {i+1})", value="\n".join(chunk), inline=False)

        # Truncate any fields that are longer than 1024 characters
            for field in words_embed.fields:
                if len(field.value) > 1024:
                    field.value = field.value[:1021] + "..."
        
            await ctx.send(embed=words_embed)

    @slash_command(name="add_word", description="Add a new word to the profanity list")
    async def add_word(self, ctx: Interaction, words: str):
        profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        added_words_file_path = os.path.join(os.path.dirname(__file__), 'added_words.json')
        with open(profanity_file_path, "r+") as profanity_file, open(added_words_file_path, "r+") as added_words_file:
            words_list = profanity_file.readlines()
            added_words_dict = json.load(added_words_file)

            if words.lower() + '\n' in words_list:
                await ctx.send("This word is already in the profanity list.")
            else:
                guild_id = str(ctx.guild.id)
                if guild_id not in added_words_dict:
                    added_words_dict[guild_id] = []
                if words.lower() not in added_words_dict[guild_id]:
                    added_words_dict[guild_id].append(words.lower())
                    added_words_file.seek(0)
                    json.dump(added_words_dict, added_words_file, indent=4)
                    await ctx.send(f"{words} has been added to the profanity list for this guild.")
                else:
                    await ctx.send("This word has already been added to the profanity list for this guild.")


    @slash_command(name="change_muted_role", description="Change the muted role for this server")
    async def change_muted_role(self, ctx: Interaction, role: nextcord.Role):
        settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You do not have the required permissions to use this command.")
            return

    # Get the guild object
        guild = ctx.guild

    # Open the settings file
        with open(settings_file_path, "r+") as f:
        # Load the existing settings
            f.seek(0)
            settings = json.load(f)

        # Check if the guild already exists in the settings
            if guild.id not in settings:
                settings[guild.id] = {}

        # Update the muted role for the guild
            settings[guild.id]["muted_role_id"] = role.id

        # Save the updated settings
            f.seek(0)
            json.dump(settings, f, indent=4)

        await ctx.send(f"The muted role for this server has been set to {role.mention}")


    @slash_command(name="help", description="Displays all available commands")
    async def help(
        self, 
        ctx:Interaction, 
    ):
        await ctx.response.send_message(
    """```General Commands
        \n/help - displays all the available commands
        \n/ban - bans a member of the discord
        \n/kick - Kicks a member from the discord
        \n/unban - Unbans a member that was banned
        \n/purge - Delete a specified number of messages
        \n/whitelist - remove or add words to the whitelist
        \n/mute - mute a specific member in discord
        \n/unmute - unmute a specific member in discord
        \n/list_banned - List all profanity words
        \n/list_whitelisted - List all whitelisted words
        \n/add_word - Add a custom word to the profanity list```""")


# AutoMod
    async def on_message(self, message: nextcord.Message):
        if message.author == self.user:
            return

        if not message.guild:
            return

        ctx = await self.get_context(message)
        await self.check_message(ctx=ctx, message=message)




    async def check_message(self, message: nextcord.Message):
        profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        whitelist_file_path = os.path.join(os.path.dirname(__file__), 'whitelist.json')
        warnings_file_path = os.path.join(os.path.dirname(__file__), 'user_warnings.json')
        settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')

        timeouts = {2: 300, 3: 3600, 4: 604800, 5: -1}  # Map offense count to timeout duration in seconds. -1 for ban.

        try:
            with open(profanity_file_path, 'r') as f:
                profanity = f.read().splitlines()
        except FileNotFoundError:
            print("File not found: profanity.txt")
            return

        try:
            with open(whitelist_file_path, 'r') as f:
                whitelist = json.load(f)
        except FileNotFoundError:
            print("File not found: whitelist.json")
            whitelist = []

        try:
            with open(warnings_file_path, 'r') as f:
                data = json.load(f)
                warning_data = data.get(str(message.author.id))
                user_warnings = warning_data.get("offenses") if warning_data else 0
                print(f"user_warnings before increment: {user_warnings}")
        except FileNotFoundError:
            print("File not found: user_warnings.json")
            user_warnings = 0

        try:
            with open(settings_file_path, "r") as f:
                settings = json.load(f)
                muted_role_id = settings.get(str(message.guild.id), {}).get("muted_role_id")
        except FileNotFoundError:
            print("File not found: settings.json")
            muted_role_id = None

        if muted_role_id:
            muted_role = message.guild.get_role(muted_role_id)

        for word in message.content.lower().split():
            if word in profanity and word not in whitelist:
                await message.delete()
                if user_warnings >= 5:
                    # If the user has reached the maximum number of offenses, ban them
                    await message.channel.send(f"{message.author.mention}, you have been banned for repeated offenses.")
                    await message.author.ban()
                    del data[str(message.author.id)]
                else:
                    # Otherwise, apply a timeout and increment the user's offense count
                    timeout_duration = timeouts.get(user_warnings + 1, 0)
                    if user_warnings >= 5:
                        # If the user has reached the maximum number of offenses, ban them
                        await message.channel.send(f"{message.author.mention}, you have been banned for repeated offenses.")
                        await message.author.ban()
                        del data[str(message.author.id)]
                    else:
                        data[str(message.author.id)] = {"timeout_end_time": time.time() + timeout_duration, "offenses": user_warnings + 1}
                        print(f"user_warnings after increment: {user_warnings + 1}")
                        if user_warnings == 0:
                            await message.channel.send(f"{message.author.mention}, your message contained a banned word. This is your warning before being timed out.")
                        elif user_warnings == 1:
                            await message.channel.send(f"{message.author.mention}, your message contained a banned word for not listening, 5m timeout")
                        elif user_warnings == 2:
                            await message.channel.send(f"{message.author.mention}, your message contained a banned word for not listening, 1 hour timeout.")
                        elif user_warnings == 3:
                            await message.channel.send(f"{message.author.mention}, your message contained a banned word for not listening, 1 week timeout.")
                        elif user_warnings == 4:
                            await message.channel.send(f"{message.author.mention}, you still dont know how to listen so enjoy the ban <3")
                            await message.author.ban(reason="Reached maximum number of offenses")
                        if timeout_duration > 0:
                            await message.author.add_roles(muted_role)
                            try:
                                await asyncio.sleep(timeout_duration)
                            finally:
                                await message.author.remove_roles(muted_role)
                        with open(warnings_file_path, 'w') as f:
                            json.dump(data, f, indent=None)



    @slash_command(description="Reset the warnings for a specified member.")
    async def resetwarnings(self, ctx: Interaction, member: nextcord.Member = None):
        warnings_file_path = os.path.join(os.path.dirname(__file__), 'user_warnings.json')
        settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')

        if member is None:
            member = ctx.author

        try:
            with open(warnings_file_path, 'r') as f:
                data = json.load(f)
                if str(member.id) in data and data[str(member.id)] != 0:
                    data[str(member.id)] = 0  # set warnings to 0
                    with open(warnings_file_path, 'w') as f:
                        json.dump(data, f)
                    await ctx.send(f"Warnings for {member.mention} have been reset.")
                else:
                    await ctx.send(f"{member.mention} already has 0 warnings.")
        except FileNotFoundError:
            print("File not found: user_warnings.json")
            await ctx.send("Failed to reset warnings.")

        try:
            with open(settings_file_path, "r") as f:
                settings = json.load(f)
                muted_role_id = settings.get(str(ctx.guild.id), {}).get("muted_role_id")
        except FileNotFoundError:
            print("File not found: settings.json")
            muted_role_id = None

        muted_role = None
        if muted_role_id:
            muted_role = ctx.guild.get_role(muted_role_id)

        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} has been unmuted.")









    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        await self.check_message(message)
        
def setup(bot : commands.Bot):
    bot.add_cog(moderation(bot))
