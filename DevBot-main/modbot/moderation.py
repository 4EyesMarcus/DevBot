from asyncio import Event
import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands
import os
import json

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#Moderation Commands

    @slash_command(name="ban", description="Ban a member of this discord", guild_ids=[1078827353444192406])
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
        
        
    @slash_command(name="unban", description="Unban a member of this discord", guild_ids=[1078827353444192406])
    async def unban(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
    ):
        if not ctx.user.guild_permissions.ban_members:
            await ctx.send("You do not have the required permissions to use this command.")
        await ctx.guild.unban(user=member)
        await ctx.response.send_message(f"{member} has been unbanned")


    @slash_command(name="kick", description="Kick a member of this discord", guild_ids=[1078827353444192406])
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



    @slash_command(name="mute", description="Mute Member in text chat", guild_ids=[1078827353444192406])
    async def mute(self, ctx: Interaction, member: nextcord.Member, reason: str):
        if not ctx.user.guild_permissions.mute_members:
            await ctx.send("You do not have the required permissions to use this command.")
        else:
            muted_role = nextcord.utils.get(ctx.guild.roles, name="muted")
            await member.add_roles(muted_role)
            await ctx.send(f"{member.mention} has been muted because {reason}")
        
        
        
    @slash_command(name="unmute", description="Unmute a member in discord",guild_ids=[1078827353444192406])
    async def unmute(self, ctx:Interaction, member:nextcord.Member):
        if not ctx.user.guild_permissions.mute_members:
            await ctx.send("You do not have the required permissions to use this command.")
        else:
            muted_role = nextcord.utils.get(ctx.guild.roles, name="muted")
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} has been unmuted.")
        
        
        
        
    @slash_command(name="help", description="Displays all available commands", guild_ids=[1078827353444192406])
    async def help(
        self, 
        ctx:Interaction, 
    ):
        await ctx.response.send_message(
    """```General Commands
        \n/help - displays all the available commands
        \n/play <keywords> - finds the song on youtube and plays it in your current channel.
        \n/queue - displays the current queue
        \n/skip - skips the current song
        \n/leave - disconnects the bot from the channel
        \n/pause - pauses the current song
        \n/resume - resumes playing the current song
        \n/ban - bans a member of the discord
        \n/kick - Kicks a member from the discord
        \n/unban - Unbans a member that was banned```""")
        

    @slash_command(name="purge", description="Delete a specified number of messages", guild_ids=[1078827353444192406])
    async def purge(self, interaction: nextcord.Interaction, limit: int):
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.response.send_message("You do not have permission to delete messages.", ephemeral=True)
            return
        await interaction.channel.purge(limit=limit + 1)
        await interaction.response.send_message(f"Deleted {limit} messages.", ephemeral=True)


    @slash_command(name="whitelist", description="Add or remove a word from the whitelist", guild_ids=[1078827353444192406])
    async def whitelist(self, ctx: Interaction, action: str = None, word: str = None):
        if not ctx.user.guild_permissions.administrator:
            await ctx.send("You do not have the required permissions to use this command.")
            return

        profanity_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        whitelist_path = os.path.join(os.path.dirname(__file__), 'whitelist.txt')
    
        try:
            with open(profanity_path, 'r') as f:
                profanity = f.read().splitlines()
        except FileNotFoundError:
            await ctx.send("File not found: profanity.txt")
            return
        
        try:
            with open(whitelist_path, 'r') as f:
                whitelist = f.read().splitlines()
        except FileNotFoundError:
            whitelist = []
    
        if action == "add":
            if word in whitelist:
                await ctx.send(f"{word} is already whitelisted.")
                return
            if word in profanity:
                profanity.remove(word)
                with open(profanity_path, 'w') as f:
                    f.write('\n'.join(profanity))
            whitelist.append(word)
            with open(whitelist_path, 'w') as f:
                f.write('\n'.join(whitelist))
            await ctx.send(f"{word} has been added to the whitelist.")
        
        elif action == "remove":
            if word not in whitelist:
                await ctx.send(f"{word} is not currently whitelisted.")
                return
            whitelist.remove(word)
            with open(whitelist_path, 'w') as f:
                f.write('\n'.join(whitelist))
            with open(profanity_path, 'a') as f:
                f.write('\n' + word)
            await ctx.send(f"{word} has been removed from the whitelist.")
    
        else:
            await ctx.send("Invalid action. Please specify 'add' or 'remove' as the first argument.")

#AutoMod
    async def check_message(self, message: nextcord.Message):
        profanity_file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        whitelist_file_path = os.path.join(os.path.dirname(__file__), 'whitelist.txt')
        warnings_file_path = os.path.join(os.path.dirname(__file__), 'user_warnings.json')

        try:
            with open(profanity_file_path, 'r') as f:
                profanity = f.read().splitlines()
        except FileNotFoundError:
            print("File not found: profanity.txt")
            return

        try:
            with open(whitelist_file_path, 'r') as f:
                whitelist = f.read().splitlines()
        except FileNotFoundError:
            print("File not found: whitelist.txt")
            whitelist = []

        try:
            with open(warnings_file_path, 'r') as f:
                data = json.load(f)
                user_warnings = data.get(str(message.author.id), 0)
        except FileNotFoundError:
            print("File not found: user_warnings.json")
            user_warnings = 0

        for word in profanity:
            if word in message.content.lower() and word not in whitelist:
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
