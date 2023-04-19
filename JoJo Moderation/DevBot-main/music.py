#Dependicies
from asyncio import Event
import nextcord
from nextcord import slash_command, Interaction, Embed
from nextcord.ext.commands import Bot
from nextcord.ext import commands
import wavelinkcord as wavelink
from wavelinkcord.player import Player
from nextcord.shard import EventItem

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

Client = nextcord.Client()

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel:
            vc = member.guild.voice_client
            if vc and vc.channel == after.channel:
                return
            await self.join_voice_channel(after.channel)

    async def join_voice_channel(self, channel):
        if not channel.guild.voice_client:
            player = await self.bot.wavelink.get_player(channel=channel, cls=Player)
            await channel.connect(reconnect=True)
            player.store("channel", channel)
            await player.set_volume(50)
        else:
            await channel.guild.voice_client.move_to(channel)


@slash_command(name="play", description="Play some music from youtube", guild_ids=[1078827353444192406])
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

@slash_command(name="skip", description="Skips the current song", guild_ids=[1078827353444192406])
async def skip(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.stop()
    await interaction.response.send_message(f"Song was skipped!!")


@slash_command(name="pause", description="Pause the current song", guild_ids=[1078827353444192406])
async def pause(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc.is_playing():
        await vc.pause()
        await interaction.response.send_message(f"Song was paused.")
    else:
        await interaction.response.send_message(f"Song is already paused!")


@slash_command(name="resume", description="Resume playing the current song", guild_ids=[1078827353444192406])
async def resume(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc.is_playing():
        await interaction.response.send_message(f"Song is already playing.")
    else:
        await vc.resume()
        await interaction.response.send_message(f"Song is resumed!")


@slash_command(name="leave", description="Leaves the vc", guild_ids=[1078827353444192406])
async def leave(interaction: nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message(f"I am disconnected!")


@slash_command(name="queue", description="Shows the current song queue", guild_ids=[1078827353444192406])
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