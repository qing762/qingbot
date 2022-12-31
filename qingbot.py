import discord
import osutools
import json
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord_together import DiscordTogether
from ossapi import Ossapi
from datetime import datetime

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True

load_dotenv()
osua = os.getenv('OSUAPI')
osuapi = Ossapi(osua)
osu = osutools.OsuClientV1(osua)
bitlyapikey = os.getenv("BITLYAPI")
token = os.getenv("DISCORDTOKEN")
hypixelapi = os.getenv("HYPIXELAPI")

extensions = ["cogs.fun", "cogs.discordutils", "cogs.information", "cogs.cogs"]

def get_prefix(bot, message):
  with open("prefixes.json", "r") as f:
    prefixes = json.loads(f.read())

  if str(message.guild.id) in prefixes:
    return commands.when_mentioned_or(prefixes[(str(message.guild.id))])(bot, message)
  else:
    return commands.when_mentioned_or(".")(bot, message)

actstream = discord.Streaming(name="w gaming", url="https://twitch.tv/qing762", platform="Twich", assets=[large_image:="reyna"], game="VALORANT", details="w gaming", start=datetime.utcnow())
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, help_command=None)
# dc = discloud.Client(discloudapitoken)

@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether(token)
    await bot.change_presence(activity=actstream)
    for extension in extensions:
        await bot.load_extension(extension)

bot.run(token)
