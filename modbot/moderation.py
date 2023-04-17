import nextcord
from nextcord.ext import commands

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#Moderation Commands
    @nextcord.slash_command(description="This kicks a user", guild_ids=[1078827353444192406])
    async def kick(self, interaction : nextcord.Interaction, user : nextcord.Member, reason):

        await interaction.send(f"{user.mention} has been kicked!")


def setup(bot : commands.Bot):
    bot.add_cog(moderation(bot))
