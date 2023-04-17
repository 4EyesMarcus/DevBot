from asyncio import Event
import nextcord
from nextcord import slash_command, Interaction
from nextcord.ext import commands

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#Moderation Commands

    @slash_command(name="kick", description="Kick a member of this discord", guild_ids=[1078827353444192406])
    async def kick(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
        reason: str = nextcord.SlashOption(name='reason', description='Please provide a reason')
    ):
        if not reason: reason = "No reason"
        await member.kick(reason=reason)
        await ctx.response.send_message(f"{member} has been kick by {ctx.user.mention} for {reason}")



    @slash_command(name="ban", description="Ban a member of this discord", guild_ids=[1078827353444192406])
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
    async def unban(
        self, 
        ctx:Interaction, 
        member: nextcord.Member = nextcord.SlashOption(name='member', description='Please provide a reason'), 
    ):
        await ctx.guild.unban(user=member)
        await ctx.response.send_message(f"{member} has been unbanned")
        

    @slash_command(name="mute", description="Mute Member in text chat", guild_ids=[1078827353444192406])
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


        
def setup(bot : commands.Bot):
    bot.add_cog(moderation(bot))
