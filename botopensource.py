import discord
import os
import asyncio
import osutools
import speedtest
import typing
import ossapi 
import requests
import time
import facebook_scraper
import json
import asyncpixel
import yt_dlp
import datetime
import itertools
import base64

from popcat_wrapper import popcat_wrapper as pop
from facebook_scraper import get_profile
from ossapi import Ossapi
from datetime import datetime
from discord.ext import commands, tasks
from itertools import cycle
from osutools.oppai import Oppai

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True

osuapi = Ossapi("OSUAPI")
osu = osutools.OsuClientV1("OSUAPI")

imgurclientid = "IMGURCLIENTID"

players = {}

token = 'BOTTOKEN'

bot = commands.Bot(command_prefix=f".", intents=intents, status=discord.Streaming(name="VALORANT ranked?",platform="Twitch", url="https://twitch.tv/qing762"))
status = cycle(['with ur mom', 'with ur dad']) 

bot.remove_command("help")

UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

@bot.event
async def on_ready():
    change_status.start()

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.command()
async def speed(ctx):
    async with ctx.typing():
        message = await ctx.reply("Please wait for 10 seconds to 1 minutes as it is performing speedtest.")
        test = speedtest.Speedtest()
        await message.edit(content="Retrieving speedtest.net server list...")
        test.get_servers()
        await message.edit(content="Retrieving the best server for speedtest...")
        test.get_best_server()
        await message.edit(content="Testing download speed...")
        download = test.download()
        await message.edit(content="Testing upload speed...")
        upload = test.upload()
        await message.edit(content="Generating results image...")
        resultimage = test.results.share()

        await message.edit(content="Generating discord embed")
        embed=discord.Embed(title="Current internet speed")
        embed.add_field(name="Download speed", value=f"{pretty_size(download)}/s")
        embed.add_field(name="Upload speed", value=f"{pretty_size(upload)}/s")
        embed.set_image(url=resultimage)
        embed.set_footer(text="Made by qing")

    await message.edit(content="Here are the results!", embed=embed)

@speed.error
async def speederror(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.reply(f"Uh-oh! Something went wrong. (Error text: `{error}`)")

@bot.command()
async def hehexd(ctx):
    await ctx.reply("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⠀⠀⠀⣠⢺⡹⣜⣳⠽⣮⢷⣻⣾⢿⣟⣿⣿⡿⣿⣽⡿⣯⢿⣹⢮⡷⣽⣭⣢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⠀⣀⡴⣟⡱⣯⡽⢮⣛⡼⣟⣿⣽⣿⣿⣿⣷⣿⣟⡿⣿⣽⢯⣿⣹⢟⡷⣯⢷⣫⢗⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⡀⣰⢯⡞⣵⡻⢶⣙⢮⡝⣿⠙⠊⠉⠙⠛⠋⠛⠉⠉⢻⡽⣯⡿⣾⡽⣯⣻⡽⣯⣟⡾⣮⢗⣧⣀⠀⠀⠀⠀⠀⠀⠀ ⢀⢔⡿⣜⡧⣿⡱⣟⣬⣛⢮⣝⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣟⣿⣿⣳⣟⡷⣯⢷⣻⣼⣻⣭⣟⠾⣧⢿⣄⠀⠀⠀⠀⠀ ⢨⣿⣻⢧⣟⣶⢻⡼⣲⡝⣾⡆⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣾⢿⣟⣿⡾⣽⢯⣟⣧⣟⣶⣛⣾⢻⡭⣟⣶⣅⡀⡀⠀⠀ ⣟⣿⣽⣿⣞⡞⣧⢻⡵⣏⣿⠛⠛⠷⣦⡀⠀⣠⣶⠟⠋⠉⠉⢻⣻⣿⣿⡿⣽⣻⣞⣷⣻⢾⡽⣞⣯⣟⡾⣵⣾⡣⠀⠀⠀ ⣿⣿⣿⣿⣿⣽⣞⣿⣿⣿⡃⠀⠀⠀⠈⢿⣶⡟⢁⣤⡀⠀⠀⠘⢿⣿⣿⣿⣟⣷⣻⢾⣽⣯⣿⣿⣾⣿⣻⣿⣷⢇⠂⠀⠀ ⠛⡿⣿⣿⣿⢿⡟⠈⠹⠿⠃⠀⠀⠀⠀⢸⣿⠀⠹⠿⠇⠀⠀⠀⠉⢿⣿⣷⣿⣿⣽⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠺⠀⠀⠀ ⠀⠁⢰⡿⠁⠸⣧⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠈⢙⣿⡿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠂⠀⠀⠀ ⠀⠀⢸⡇⣀⣤⣙⢷⣤⣀⣀⣀⣀⣠⣴⡿⣬⣿⣦⣄⡀⠀⠀⠀⣀⣴⠾⢃⣀⣄⡍⠉⠘⠙⠳⢿⣿⣿⡿⡟⠁⠀⠀⠀⠀ ⠀⠀⠘⣿⣣⢷⣫⠷⡎⠉⢻⣿⡛⠭⡑⠰⢄⠒⠬⣙⣻⣿⠛⠛⠋⢡⡞⣽⡺⡼⣝⣳⡀⠀⠀⢸⡟⠛⠉⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⣷⢏⣾⡱⣿⣹⠀⠘⣯⢙⠻⠶⠿⠶⠿⡛⢛⣩⡿⠀⠀⠀⢸⡽⣖⡻⣝⢾⡱⡏⠀⢀⣿⣥⣄⣀⡀⠀⠀⠀⠀⠀ ⠀⠀⠀⠘⣿⣲⣻⠵⠃⠀⠀⠈⠻⢦⣭⣦⣧⣼⡴⠟⠋⠀⠀⠀⠀⠘⢳⣭⢟⡾⣭⢗⠃⢀⣾⣇⠦⣐⣦⢟⠳⢦⡀⠀⠀ ⠀⠀⠀⠀⠈⢿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠚⠑⠁⠀⣠⣿⡿⢉⣿⠿⣥⣮⣦⣧⣙⣆⠀ ⠀⠀⠀⠀⠀⢠⣽⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⡟⢁⢆⡽⡃⣾⠏⠷⣆⠆⡍⠻⡆ ⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣦⣄⣀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡃⣾⠱⡐⣿⢈⠒⡹⢧⡌⢃⡇ ⠀⠀⠀⠀⠀⢀⣼⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣭⡿⠁⣿⣿⣿⣿⣇⠱⡐⢿⣄⠣⡐⢛⡧⢡⡇ ⠀⠀⠀⠀⢀⣾⣿⣿⣆⠈⢿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣛⣭⣷⣿⣿⣿⠁⢀⣿⣿⣿⣿⣿⠢⠜⡸⣧⠣⡙⢢⣟⡞⠀ ⠀⠀⠀⠀⣾⣿⣿⣿⡿⠀⢸⣿⣧⡻⣿⣿⠿⣛⣯⣷⣿⣿⣿⣿⣿⣿⣿⡇⠀⣸⣿⣿⣿⣿⣿⣇⠚⡔⣿⢡⣙⡼⠋⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠛⠛⠛⠛⠛⠓⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠒⠒⠛⠛⠛⠛⠛⠛⠓⠓⠚⠛⠋⠁⠀⠀⠀")

@bot.command(aliases=["osu", "oprofile", "osuprof"])
async def osuprofile(ctx, osuname : typing.Optional[str]):
    async with ctx.typing():
        if osuname == None:
            osuname = ctx.author.name

        prof = osu.fetch_user(username=osuname)
        best = prof.fetch_best()[:1]
        for score in best:
            beatmap = score.fetch_map()

        today = datetime.utcnow()
        now = today.strftime("%d/%m/%Y %H:%M:%S")

        joinedosu = prof.join_date
        joinosudate = joinedosu.strftime("%d/%m/%Y %H:%M:%S")

        embed=discord.Embed(url=f"https://osu.ppy.sh/users/{prof.username}")
        embed.set_thumbnail(url=prof.avatar_url)
        embed.add_field(name="Profile ID", value=f"{prof.id}", inline=True)
        embed.add_field(name="Level", value=f"{prof.level}", inline=True)
        embed.add_field(name="Playcount", value=f"{prof.play_count}", inline=True)
        embed.add_field(name="Joined osu during", value=f"{joinosudate} GMT", inline=False)
        embed.add_field(name="Total PPs earned", value=f"{prof.pp}", inline=False)
        embed.add_field(name="Global rank", value=f"#{prof.rank}", inline=True)
        embed.add_field(name="Country rank", value=f"{prof.country} #{prof.country_rank}", inline=True)
        embed.add_field(name="Accuracy", value=f"{round(prof.accuracy, 2)}%", inline=True)
        embed.add_field(name="SSH Count | SS Count | SH Count | S Count | A Count :", value=f"{prof.ssh_count} SSH | {prof.ss_count} SS | {prof.sh_count} SH | {prof.s_count} S | {prof.a_count} A", inline=False)
        embed.add_field(name="Top map played | PP earned | Score | Mod used :", value=f"{beatmap} | {score.pp} | {score.score} | {score.mods}", inline=False)
        embed.set_footer(text=f"Made by qing | Session ID: {base64.b64encode(os.urandom(3))} | Timestamp: {now} GMT | (Note: The data might not be 100% same as the picture bcuz of the rate limiting function implemented by osu!)")
        embed.set_author(name=f"osu! stats for {prof.username}", icon_url=f"https://flagcdn.com/w2560/{prof.country.lower()}.png")
        embed.set_image(url=f"http://lemmmy.pw/osusig/sig.php?colour=hex8866ee&uname={prof.username}&pp=1&countryrank&removeavmargin&flagshadow&darktriangles&opaqueavatar&avatarrounding=4&onlineindicator=undefined&xpbar&xpbarhex")
    await ctx.send(embed=embed)

@osuprofile.error
async def osuprofile_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        async with ctx.typing():
            await ctx.reply(f"Uh-oh! Something went wrong. Please double check your name entered (Error text: `{error}`)")

@bot.command(pass_context=True, aliases=["user", "userprofile", "userprof", "whois"])
async def userinfo(ctx, user: typing.Optional[discord.Member]):
    async with ctx.typing():
        if user == None:
            user = ctx.author

        joinedat = user.joined_at
        joinedtime = joinedat.strftime("%d/%m/%Y %H:%M:%S")

        createdat = user.created_at
        createdtime = createdat.strftime("%d/%m/%Y %H:%M:%S")

        nitrosince = user.premium_since
        if bool(nitrosince) == True:
            nitro = nitrosince.strftime("%d/%m/%Y %H:%M:%S")
            finalnitro = f"{nitro} GMT"
        else:
            pass

        userid = await bot.fetch_user(f"{user.id}")

        rolelist = []
        for roles in user.roles:
            if roles.name != "@everyone":
                rolelist.append(f"<@&{roles.id}>")

        b = ','.join(rolelist)

        today = datetime.utcnow()
        now = today.strftime("%d/%m/%Y %H:%M:%S")

        embed=discord.Embed(colour=user.color)
        embed.add_field(name="Username:", value=f"{user.name}", inline=True)
        embed.add_field(name="Server Username:", value=f"{user.display_name}", inline=True)
        embed.add_field(name="Discriminator:", value=f"{user.discriminator}", inline=True)
        embed.add_field(name="Is bot?", value=f"{user.bot}", inline=True)
        embed.add_field(name="Status:", value=f"{user.raw_status}")
        embed.add_field(name="User ID:", value=f"{user.id}", inline=True)
        embed.add_field(name="Status:", value=f"{str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}")
        embed.add_field(name=f"Roles ({len(rolelist)}):", value=f"".join([b]))
        embed.add_field(name="Top role:", value=f"{user.top_role.mention}", inline=True)
        embed.add_field(name="Nitro?", value=f"{bool(user.premium_since)}", inline=True)
        embed.add_field(name="Nitro since:", value=f"{finalnitro if bool(user.premium_since) == True else 'N/A'}")
        embed.add_field(name="Account created at:", value=f"{createdtime} GMT", inline=True)
        embed.add_field(name="Joined server at:", value=f"{joinedtime} GMT", inline=True)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"Made by qing | Session ID: {base64.b64encode(os.urandom(3))} | Timestamp: {now} GMT")
        embed.set_author(name=f"User information for @{user.name}", icon_url=user.avatar.url)
        embed.set_image(url=userid.banner.url if userid.banner else 'https://qingbotcommand.netlify.app/shabi.webp')
    await ctx.reply(embed=embed)

@bot.command(pass_context=True, aliases=["server", "serverprofile", "serverprof"])
async def serverinfo(ctx):
    async with ctx.typing():
        simple = ctx.guild

        createat = simple.created_at.strftime("%d/%m/%Y %H:%M:%S")

        statuses = [len(list(filter(lambda m: str(m.status) == "online", simple.members))),
					len(list(filter(lambda m: str(m.status) == "idle", simple.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", simple.members))),
					len(list(filter(lambda m: str(m.status) == "offline", simple.members)))]

        today = datetime.utcnow()
        now = today.strftime("%d/%m/%Y %H:%M:%S")

        embed=discord.Embed(title=f"Server information for {simple.name}")
        embed.add_field(name="Server name:", value=f"{simple.name}", inline=True)
        embed.add_field(name="Server description:", value=f"{simple.description}", inline=True)
        embed.add_field(name="Server ID", value=f"{simple.id}", inline=True)
        embed.add_field(name="Created at:", value=f"{createat}", inline=True)
        embed.add_field(name="Owner", value=f"{simple.owner}", inline=True)
        embed.add_field(name="Owner ID", value=f"{simple.owner.id}", inline=True)
        embed.add_field(name="Total members count:", value=f"{len(simple.members)}", inline=True)
        embed.add_field(name="Humans count:", value=f"{len(list(filter(lambda m: not m.bot, simple.members)))}")
        embed.add_field(name="Bots count:", value=f"{len(list(filter(lambda m: m.bot, simple.members)))}", inline=True)
        embed.add_field(name="Unavailable?", value=f"{bool(simple.unavailable)}", inline=True)
        embed.add_field(name="Chunked?", value=f"{bool(simple.chunked)}", inline=True)
        embed.add_field(name="Widget enabled?:", value=f"{simple.widget_enabled}", inline=True)
        embed.add_field(name="Categories count:", value=f"{len(simple.categories)}", inline=True)
        embed.add_field(name="Member statuses count:", value=f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}")
        embed.add_field(name="Text channels count:", value=f"{len(simple.text_channels)}", inline=True)
        embed.add_field(name="Voice channels count:", value=f"{len(simple.voice_channels)}", inline=True)
        embed.add_field(name="Stage channels count:", value=f"{len(simple.stage_channels)}", inline=True)
        embed.add_field(name="Nitro boost progress bar enabled?", value=f"{bool(simple.premium_progress_bar_enabled)}", inline=True)
        embed.add_field(name="Nitro boost subscriber role:", value=f"{simple.premium_subscriber_role.mention}", inline=True)
        embed.add_field(name="Nitro boost subscription count", value=f"{simple.premium_subscription_count}", inline=True)
        embed.add_field(name="Sticker limit:", value=f"{simple.sticker_limit}", inline=True)
        embed.add_field(name="NSFW level:", value=f"{simple.nsfw_level}", inline=True)
        embed.add_field(name="Bitrate limit:", value=f"{float(simple.bitrate_limit)}", inline=True)
        embed.add_field(name="Non-nitro members file size limit:", value=f"{pretty_size(simple.filesize_limit)} ", inline=True)
        embed.add_field(name="Verification level", value=f"{simple.verification_level}", inline=True)
        embed.add_field(name="Max members:", value=f"{simple.max_members}", inline=True)
        embed.add_field(name="Max presences:", value=f"{simple.max_presences}", inline=True)
        embed.add_field(name="Explicit content filter:", value=f"{simple.explicit_content_filter}", inline=True)
        embed.add_field(name="Notification settings:", value=f"{simple.default_notifications}", inline=True)
        embed.add_field(name="Max video channels users:", value=f"{simple.max_video_channel_users}", inline=True)
        embed.add_field(name="Vanity invite url:", value=f"{simple.vanity_url if bool(simple.vanity_url) == False else 'N/A'}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.set_footer(text=f"Made by qing | Session ID: {base64.b64encode(os.urandom(3))} | Timestamp: {now} GMT")
        embed.set_thumbnail(url=simple.icon)
        embed.set_author(name=f"Request made by {ctx.author}", icon_url=ctx.author.avatar.url)
        embed.set_image(url=simple.splash)
    await ctx.reply(embed=embed)

@bot.command()
async def debug(ctx, osuname):
    async with ctx.typing():
        if osuname == None:
            osuname = ctx.author.name

        prof = osu.fetch_user(username=osuname)
    await ctx.send(f"{prof.playtime}")

@bot.command()
async def github(ctx, githubname = None):
    async with ctx.typing():
        message = await ctx.reply(f"Fetching github profile with the name {githubname}")
        if githubname == None:
            githubname = ctx.author.name
        await message.edit(content="Fetching avatar...")
        gavatar = await pop.github(githubname, property="avatar")
        await message.edit(content="Fetching url...")
        gurl = await pop.github(githubname, property="url")
        await message.edit(content="Fetching account type...")
        gacctype = await pop.github(githubname, property="account_type")
        await message.edit(content="Fetching name...")
        gname = await pop.github(githubname, property="name")
        await message.edit(content="Fetching company...")
        gcompany = await pop.github(githubname, property="company")
        await message.edit(content="Fetching email...")
        gemail = await pop.github(githubname, property="email")
        await message.edit(content="Fetching blog...")
        gblog = await pop.github(githubname, property="blog")
        await message.edit(content="Fetching location...")
        glocation = await pop.github(githubname, property="location")
        await message.edit(content="Fetching account created time...")
        gca = await pop.github(githubname, property="created_at")
        await message.edit(content="Fetching last updated time...")
        gua = await pop.github(githubname, property="updated_at")
        await message.edit(content="Fetching bio...")
        gbio = await pop.github(githubname, property="bio")
        await message.edit(content="Fetching twitter...")
        gtwitter = await pop.github(githubname, property="twitter")
        await message.edit(content="Fetching public repos...")
        gpubrepo = await pop.github(githubname, property="public_repos")
        await message.edit(content="Fetching public gists...")
        gpubgist = await pop.github(githubname, property="public_gists")
        message.edit(content="Fetching followers...")
        gfollowers = await pop.github(githubname, property="followers")
        await message.edit(content="Fetching following...")
        gfollowing = await pop.github(githubname, property="following")

        embed = discord.Embed(colour=ctx.author.colour, title=f"Github profile for {gname}", url=gurl)
        embed.add_field(name="Profile name", value=gname, inline=True)
        embed.add_field(name="Account type", value=gacctype, inline=True)
        embed.add_field(name="Email", value=gemail, inline=True)
        embed.add_field(name="Twitter", value=gtwitter, inline=True)
        embed.add_field(name="Blog", value=gblog, inline=True)
        embed.add_field(name="Bio", value=gbio, inline=False)
        embed.add_field(name="Company", value=gcompany, inline=True)
        embed.add_field(name="Location", value=glocation, inline=True)
        embed.add_field(name="Created at", value=gca, inline=True)
        embed.add_field(name="Last updated at", value=gua, inline=True)
        embed.add_field(name="Followers count", value=gfollowers, inline=True)
        embed.add_field(name="Following count", value=gfollowing, inline=True)
        embed.add_field(name="Public repos count", value=gpubrepo, inline=True)
        embed.add_field(name="Public gists count", value=gpubgist, inline=True)
        embed.set_thumbnail(url=gavatar)
    await message.edit(content="Here you go!", embed=embed)    

@bot.command()
async def osuranked(ctx):
    await ctx.reply("https://osu.kiwec.net/ | https://discord.gg/dMBCAXNQAN")

@bot.command()
async def osulazer(ctx):
    await ctx.reply("https://github.com/ppy/osu/releases/download/2022.1008.2/install.exe (PC) | https://github.com/ppy/osu/releases/download/2022.1008.2/sh.ppy.osulazer.apk (Android)")

@bot.command()
async def uncover(ctx, user : discord.Member = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        pfp = user.display_avatar.url
        image = await pop.uncover(pfp)

    await ctx.send(image)

@bot.command()
async def drip(ctx, user : discord.Member = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        pfp = user.display_avatar.url
        image = await pop.drip(pfp)

    await ctx.send(image)

bot.run(token)