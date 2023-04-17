#Dependicies
import nextcord
from nextcord import slash_command
from nextcord.ext import commands
import wavelinkcord as wavelink
from nextcord.shard import EventItem

bot_version = "0.0.1"

intents = nextcord.Intents.default()
intents.voice_states = True
intents.members = True  
intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True
intents.members = True
intents.message_content = True
intents.presences = True


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@slash_command(guild_ids=[1078827353444192406])
async def play(interaction: nextcord.Interaction, search: str):
    query = await wavelink.YouTubeTrack.search(search, return_first=True)
    destination = interaction.user.voice.channel

    if not interaction.guild.voice_client:
        vc: wavelink.Player = await destination.connect(cls=wavelink.Player)
    else:
        vc: wavelink.Player = interaction.guild.voice_client

    if vc.queue.is_empty and not vc.is_playing():
        await vc.play(query)
        await interaction.response.send_message(f"Now Playing {vc.current.title}")
    else:
        await vc.queue.put_wait(query)
        await interaction.response.send_message(f"Song was added to the queue")

@slash_command(guild_ids=[1078827353444192406])
async def skip(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.stop()
    await interaction.response.send_message(f"Song was skipped!!")

@slash_command(guild_ids=[1078827353444192406])
async def pause(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc.is_playing():
        await vc.pause()
        await interaction.response.send_message(f"Song was paused.")
    else:
        await interaction.response.send_message(f"Song is already paused!")

@slash_command(guild_ids=[1078827353444192406])
async def resume(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc.is_playing():
        await interaction.response.send_message(f"Song is already playing.")
    else:
        await vc.resume()
        await interaction.response.send_message(f"Song is resumed!")

@slash_command(guild_ids=[1078827353444192406])
async def leave(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message(f"I am disconnected!")

@slash_command(guild_ids=[])
async def queue(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if not vc.queue.is_empty:
        song_counter = 0
        songs = []
        queue = vc.queue.copy()
        embed = nextcord.Embed(title="Queue")
        for song in queue:
            song_counter += 1
            songs.append(song)
            embed.add_field(name=f"[{song_counter}] Duration {round((song.duration / 1000) / 60, 2)}", value=f"{song.title}", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("The queue is empty!")
        

def setup(bot : commands.Bot):
    bot.add_cog(music(bot))