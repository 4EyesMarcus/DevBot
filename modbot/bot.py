#Dependicies
import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
from nextcord.shard import EventItem


intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix="/", intents=intents)


extensions = [
    "moderation",
    "music"
]

if __name__ == "__main__":
    for ext in extensions:
        bot.load_extension(ext)

#Start/Status
@bot.event
async def on_ready():
    print("Bot Ready!")
    bot.loop.create_task(on_node())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{songs[random.randint(0, 5)]}"))
    
async def on_ready():
    node: wavelink.Node = wavelink.Node(uri='http://lavalink.clxud.pro:2333', password='youshallnotpass')
    await wavelink.NodePool.connect(client=bot, nodes=[node], spotify=sc)

    
#Join Message
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1078827353897185312)
    await channel.send(f"Welcome to {member.guild.name}, {member.mention}!")


#Leave message
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1078827353897185312)
    await channel.send(f"Everyone wave and say bye to {member.mention}!")



bot.run("MTA5Mjg5MzkzMjU0OTA2NjgwMg.GCqnGd.TTbIoXmtUI-fiPXypo6jNWvsNZ0hmNOXgDJhvw")