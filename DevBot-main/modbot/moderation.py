from asyncio import Event
import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands
import os

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#Moderation Commands

    @slash_command(name="ban", description="Ban a member of this discord", guild_ids=[1078827353444192406])
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
        reason: str = nextcord.SlashOption(name='reason', description='Please provide a reason')
    ):
        if not reason: reason = "No reason"
        await member.ban(reason=reason)
        await ctx.response.send_message(f"{member} has been banned by {ctx.user.mention} for {reason}")
        
        
    @slash_command(name="unban", description="Unban a member of this discord", guild_ids=[1078827353444192406])
    @commands.has_permissions(ban_members=True)
    async def unban(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
    ):
        await ctx.guild.unban(user=member)
        await ctx.response.send_message(f"{member} has been unbanned")
        

    @slash_command(name="mute", description="Mute Member in text chat", guild_ids=[1078827353444192406])
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx: Interaction, member: nextcord.Member, reason: str):
        muted_role = nextcord.utils.get(ctx.guild.roles, name="muted")
        await member.add_roles(muted_role)
        await ctx.send(f"{member.mention} has been muted because {reason}")
        
        
        
    @slash_command(name="unmute", description="Unmute a member in discord",guild_ids=[1078827353444192406])
    async def unmute(self, ctx:Interaction, member:nextcord.Member):
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


#Banned Words Text File
    async def check_message(self, message: nextcord.Message):
        user_warnings = {} # dictionary to keep track of how many warnings each user has received
        file_path = os.path.join(os.path.dirname(__file__), 'profanity.txt')
        try:
            with open(file_path, 'r') as f:
                profanity = f.read().splitlines()
        except FileNotFoundError:
            print("File not found: profanity.txt")
            return
    
        for word in profanity:
            if word in message.content.lower():
                user_id = message.author.id
                if user_id in user_warnings:
                    user_warnings[user_id] += 1
                    if user_warnings[user_id] == 2:
                        muted_role = nextcord.utils.get(message.guild.roles, name='muted') # Replace 'Muted' with the name of your muted role
                        if muted_role:
                            await message.author.add_roles(muted_role, reason="Message contained a banned word.")
                            await message.channel.send(f"{message.author.mention}, you have been muted for using a banned word.")
                        else:
                            await message.channel.send("Muted role not found.")
                    elif user_warnings[user_id] >= 3:
                        await message.author.ban(reason="Message contained a banned word. Next time you will be banned!")
                        await message.channel.send(f"{message.author.mention}, you have been banned for using a banned word.")
                else:
                    user_warnings[user_id] = 1



    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        await self.check_message(message)
        
def setup(bot : commands.Bot):
    bot.add_cog(moderation(bot))
