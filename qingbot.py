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

'''
# Deprecated
@bot.command()
async def badminton(ctx, cmdname : str = None, user : discord.User | str = None, input : str = None):
    locationcmd = ["setlocation", "setplace"]
    addcmd = ["add", "addpeople"]
    boyinput = ["boy", "man"]
    girlinput = ["girl", "woman"]
    
    if cmdname == None:
        await ctx.reply("Please enter a valid command!")
    elif cmdname == "setprice":
        with open("badminton.json", "r") as file:
            data = json.load(file)
            data['price'].__add__(user)

        with open("badminton.json", "w") as file:
            json.dump(data, file)

        await ctx.reply(f"Set {user} as the price")

    elif cmdname in locationcmd:
        with open("badminton.json", "r") as file:
            data = json.load(file)
            data['location'].__add__(user)

        with open("badminton.json", "w") as file:
            json.dump(data, file)

        await ctx.reply(f"Set {user} as the location")

    elif cmdname == "settime":
        with open("badminton.json", "r") as file:
            data = json.load(file)
            data['time'].__add__(user)

        with open("badminton.json", "w") as file:
            json.dump(data, file)

        await ctx.reply(f"Set {user} as the time")

    elif cmdname == "setduration":
        with open("badminton.json", "r") as file:
            data = json.load(file)
            data['duration'].__add__(user)

        with open("badminton.json", "w") as file:
            json.dump(data, file)

        await ctx.reply(f"Set {user} as the duration")

    elif cmdname in addcmd:
        if isinstance(user, discord.User):
            if input in boyinput:
                with open("badminton.json", "r") as file:
                        data = json.load(file)
                data['boy'].append(user.id)
                with open("badminton.json", "w") as file:
                    json.dump(data, file)

        if isinstance(user, discord.User):
            if input in girlinput:
                with open("badminton.json", "r") as file:
                        data = json.load(file)
                data['girl'].append(user.id)
                with open("badminton.json", "w") as file:
                    json.dump(data, file)

        if isinstance(user, str):
            if input in boyinput:
                with open("badminton.json", "r") as file:
                        data = json.load(file)
                data['boy'].append(str(user))
                with open("badminton.json", "w") as file:
                    json.dump(data, file)

        if isinstance(user, str):
            if input in girlinput:
                with open("badminton.json", "r") as file:
                        data = json.load(file)
                data['girl'].append(str(user))
                with open("badminton.json", "w") as file:
                    json.dump(data, file)

            else:
                await ctx.reply("Please enter a valid gender!")          
        else:
            await ctx.reply("Please enter a valid discord user or name!")
        
        with open("badminton.json", "r") as file:
            data = json.load(file)
            boydata = data["boy"]
            girldata = data["girl"]
            place = data["location"]
            price = data["price"]
            numboy = len(boydata)
            numgirl = len(girldata)
            duration = data["duration"]
            mt = duration / numboy
        embed = discord.Embed(color=ctx.author.color, title=f"Badminton matches for {pendulum.now().next(pendulum.SATURDAY).strftime('%Y-%m-%d')}")
        embed.add_field(name="Location", value=place if place != "" else "N/A")
        embed.add_field(name="Time", value=time if time != "" else "N/A")
        embed.add_field(name="Duration", value=duration if duration!= "" else "N/A")
        embed.add_field(name="Price", value=f"RM{price} (RM{mt} each)" if price != "" else "N/A")
        embed.add_field(name=f"Boys ({numboy})", value=", ".join(boydata))
        embed.add_field(name=f"Girls ({numgirl})", value=", ".join(girldata))
        embed.set_footer(text="Made with ❤️ by qing")
        await ctx.reply(embed=embed)
''' 

bot.run(token)