from asyncio import Event
import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands
import os
import json

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.whitelist = {}

        self.profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        self.whitelist_file_path = os.path.join(os.path.dirname(__file__), 'whitelist.json')
        self.warnings_file_path = os.path.join(os.path.dirname(__file__), 'user_warnings.json')

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






#Moderation Commands

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
        with open(profanity_file_path, "r+") as profanity_file:
            words_list = profanity_file.readlines()
            if words.lower() + '\n' in words_list:
                await ctx.send("This word is already in the profanity list.")
            else:
                profanity_file.write(words.lower() + '\n')
                await ctx.send(f"{words} has been added to the profanity list.")


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


#AutoMod
    async def check_message(self, message: nextcord.Message):
        profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        whitelist_file_path = os.path.join(os.path.dirname(__file__), 'whitelist.json')
        warnings_file_path = os.path.join(os.path.dirname(__file__), 'user_warnings.json')

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
                user_warnings = data.get(str(message.author.id), 0)
        except FileNotFoundError:
            print("File not found: user_warnings.json")
            user_warnings = 0

        for word in message.content.lower().split():
            if word in self.profanity and word not in self.whitelist:
                if user_warnings >= 2:
                    muted_role = nextcord.utils.get(message.guild.roles, name='muted')
                    if muted_role:
                        await message.author.add_roles(muted_role, reason="Message contained a banned word.")
                        await message.channel.send(f"{message.author.mention}, you have been muted for using a banned word.")
                    else:
                        await message.channel.send("Muted role not found.")
                elif user_warnings >= 1:
                    await message.channel.send(f"{message.author.mention}, your message contains a banned word. This is your final warning before being muted.")
                else:
                    await message.channel.send(f"{message.author.mention}, your message contains a banned word. Please refrain from using it.")

                user_warnings += 1
                data[str(message.author.id)] = user_warnings

                with open(warnings_file_path, 'w') as f:
                    json.dump(data, f)

                break




   




    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        await self.check_message(message)
        
def setup(bot : commands.Bot):
    bot.add_cog(moderation(bot))
