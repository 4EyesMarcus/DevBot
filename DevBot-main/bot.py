#Dependicies
import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.all()
client = nextcord.Client()

bot = commands.Bot(command_prefix="/", intents=intents)

extensions = [
  "moderation",
  "tickets",
]

if __name__ == "__main__":
  for ext in extensions:
    print(f"Loading {ext}")
    bot.load_extension(ext)

DEFAULT_CHANNEL_ID = None  # This will store the default channel ID


#Start/Status
@bot.event
async def on_ready():
  print("Bot Online")
  await bot.change_presence(activity=nextcord.Activity(
    type=nextcord.ActivityType.listening, name=f"/help for commands"))


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


bot.run(
  "")
