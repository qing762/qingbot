import discord
import os
import asyncio
import osutools
import random
import aniso8601
import urlexpander
import contextlib
import io
import string
import requests
import pyshorteners
import json
import json
import asyncpixel
import datetime
import base64
import textwrap

from dotenv import load_dotenv
from traceback import format_exception
from skingrabber import skingrabber
from discord_together import DiscordTogether
from popcat_wrapper import popcat_wrapper as pop
from ossapi import Ossapi
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True

load_dotenv()
players = {}
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

osua = os.getenv('OSUAPI')
osuapi = Ossapi(osua)
osu = osutools.OsuClientV1(osua)
bitlyapikey = os.getenv("BITLYAPI")
token = os.getenv("DISCORDTOKEN")
hypixelapi = os.getenv("HYPIXELAPI")

def get_prefix(client, message):
  with open("prefixes.json", "r") as f:
    prefixes = json.loads(f.read())

  if str(message.guild.id) in prefixes:
    return commands.when_mentioned_or(prefixes[(str(message.guild.id))])(client, message)
  else:
    return commands.when_mentioned_or(".")(client, message)

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

def pretty_size(bytes, units=UNITS_MAPPING):
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

activitystream = discord.Streaming(name="w gaming", url="https://twitch.tv/qing762", platform="Twich", assets=[large_image:="reyna"], game="VALORANT", details="w gaming", start=datetime.utcnow())
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True, help_command=None)

bot.remove_command("help")

@bot.event
async def on_ready():
    bot.togetherControl = await DiscordTogether(token)
    await bot.change_presence(activity=activitystream)

@bot.command(aliases=["osu", "oprofile", "osuprof"])
async def osuprofile(ctx, osuname = None):
    async with ctx.typing():
        if osuname == None:
            osuname = ctx.author.name
        else:
            osuname = osuname

        try:
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
            embed.set_footer(text=f"Made by qing | Timestamp: {now} GMT | (Note: The data might not be 100% same as the picture bcuz of the rate limiting function implemented by osu!)")
            embed.set_author(name=f"osu! stats for {prof.username}", icon_url=f"https://flagcdn.com/w2560/{prof.country.lower()}.png")
            embed.set_image(url=f"http://lemmmy.pw/osusig/sig.php?colour=hex8866ee&uname={prof.username}&pp=1&countryrank&removeavmargin&flagshadow&darktriangles&opaqueavatar&avatarrounding=4&onlineindicator=undefined&xpbar&xpbarhex")
            await ctx.send(embed=embed)
        except Exception:
            await ctx.reply(f"Uh-oh! Something went wrong. Please double check your name enterred if it is a valid osu username!")

@bot.command(pass_context=True, aliases=["user", "userprofile", "userprof", "whois"])
async def userinfo(ctx, user: discord.User = None):
    async with ctx.typing():
        guild = bot.get_guild(ctx.guild.id)
        if user == None:
            user = ctx.author

        elif guild.get_member(user.id) is not None:
            user: discord.Member
            joinedat = user.joined_at
            joinedtime = joinedat.strftime("%d/%m/%Y %H:%M:%S")
            joingmt = f"{joinedtime} GMT"
            nitrosince = user.premium_since
            if bool(nitrosince) == True:
                nitro = nitrosince.strftime("%d/%m/%Y %H:%M:%S")
                finalnitro = f"{nitro} GMT"
            else:
                pass
            rolelist = []
            for roles in user.roles:
                if roles.name != "@everyone":
                    rolelist.append(f"<@&{roles.id}>")
            b = ','.join(rolelist)
        else:
            user: discord.User

        createdat = user.created_at
        createdtime = createdat.strftime("%d/%m/%Y %H:%M:%S")

        userid = await bot.fetch_user(f"{user.id}")

        today = datetime.utcnow()
        now = today.strftime("%d/%m/%Y %H:%M:%S")

        embed=discord.Embed(colour=user.color)
        embed.add_field(name="Username:", value=f"{user.name}", inline=True)
        embed.add_field(name="Server Username:", value=f"{user.display_name}", inline=True)
        embed.add_field(name="Discriminator:", value=f"{user.discriminator}", inline=True)
        embed.add_field(name="Is bot?", value=f"{user.bot}", inline=True)
        embed.add_field(name="Status:", value=f"{user.raw_status if guild.get_member(user.id) is not None else 'N/A'}")
        embed.add_field(name="User ID:", value=f"{user.id}", inline=True)

        if guild.get_member(user.id) is not None:
            embed.add_field(name="Presence:", value=f"{str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}")
        else:
            pass

        embed.add_field(name=f"Roles ({len(rolelist) if guild.get_member(user.id) is not None else '0'}):", value=f"".join([b]) if guild.get_member(user.id) is not None else 'N/A')
        
        embed.add_field(name="Top role:", value=f"{user.top_role.mention if guild.get_member(user.id) is not None else 'N/A'}", inline=True)
        embed.add_field(name="Nitro?", value=f"{bool(user.premium_since) if guild.get_member(user.id) is not None else 'N/A'}", inline=True)
        embed.add_field(name="Nitro since:", value=f"{finalnitro if guild.get_member(user.id) is not None else 'N/A'}")
        embed.add_field(name="Account created at:", value=f"{createdtime} GMT", inline=True)
        embed.add_field(name="Joined server at:", value=f"{joingmt if guild.get_member(user.id) is not None else 'N/A'}", inline=True)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text=f"Made by qing | Timestamp: {now} GMT")
        embed.set_author(name=f"User information for @{user.name}", icon_url=user.avatar.url)
        embed.set_image(url=userid.banner.url if userid.banner else 'https://qingbotcommand.netlify.app/shabi.webp')
    await ctx.reply(embed=embed)

@bot.command(aliases=["server", "serverprofile", "serverprof", "serverinf"])
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
async def github(ctx, githubname = None):
    async with ctx.typing():
        message = await ctx.reply(f"Fetching github profile with the name {githubname}")
        if githubname == None:
            githubname = ctx.author.name
        else:
            githubname == githubname

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
async def uncover(ctx, user : discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        pfp = user.display_avatar.url
        image = await pop.uncover(pfp)

    await ctx.send(image)

@bot.command()
async def drip(ctx, user : discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        pfp = user.display_avatar.url
        image = await pop.drip(pfp)

    await ctx.send(image)

@bot.command()
async def alert(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please enter a valid text")
        else:
            text = text

        finaltext = text.replace(" ", "+")
        l = f'https://api.popcat.xyz/alert?text={finaltext}'
    await ctx.reply(l)
    
@bot.command()
async def mcskinrendered(ctx, username = None):
    async with ctx.typing():
        sg = skingrabber()
        if username == None:
            await ctx.reply("Your username cannot be blank!")
        else:
            try:
                await ctx.reply(sg.get_skin_rendered(user=username))
            except Exception:
                await ctx.reply("An error occured! Please try checking your input if its a valid Minecraft username.")
                return

@bot.command()
async def mcskinraw(ctx, username = None):
    async with ctx.typing():
        sg = skingrabber()
        if username == None:
            await ctx.reply("Your username cannot be blank!")
        else:
            try:
                await ctx.reply(sg.get_skin(user=username))
            except Exception:
                await ctx.reply("An error occured! Please try checking your input if its a valid Minecraft username.")
        
@bot.command()
async def pi(ctx):
    await ctx.reply(f"π = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925892354201995611212902196086403441815981362977477130996051870721134999999837297804995105973173281609631859502445945534690830264252230825334468503526193118817101000313783875288658753320838142061717766914730359825349042875546873115956286388235378759375195778185778053217122680661300192787661119590921642019893809525720106548586327886593615338182796823030195203530185296899577362259941389124972177528347913151557485724245415069595082953311686172785588907509838175463746493931925506040092770167113900984882401285836160356370766010471018194295559619894676783744944825537977472684710404753464620804668425906949129331367702898915210475216205696602405803815019351125338243003558764024749647326391419927260426992279678235478163600934172164121992458631503028618297455570674983850549458858692699569092721079750930295532116534498720275596023648066549911988183479775356636980742654252786255181841757467289097777279380008164706001614524919217321721477235014144197356854816136115735255213347574184946843852332390739414333454776241686251898356948556209921922218427255025425688767179049460165346680498862723279178608578438382796797668145410095388378636095068006422512520511739298489608412848862694560424196528502221066118630674427862203919494504712371378696095636437191728746776465757396241389086583264599581339047802")

@bot.command()
async def say(ctx, *, message = None):
    async with ctx.typing():
        if message == None:
            await ctx.reply("Please pass in a required argument")
        else:
            await ctx.send(f"{ctx.author.mention} wants to say : ```{message}```")

@bot.command()
async def ping(ctx):
    resp = await ctx.reply('Pong! Loading...')
    diff = resp.created_at - ctx.message.created_at
    totalms = 1000 * diff.total_seconds()
    emb = discord.Embed()
    emb.title = "Pong!"
    emb.add_field(name="Your message time", value=f"{totalms}ms")
    emb.add_field(name="The API latency", value=f"{(1000 * bot.latency):.1f}ms")
    emb.set_footer(text="Made with ❤️ by qing")
    await resp.edit(embed=emb, content="")

@bot.command()
async def whenisthenextmcufilm(ctx):
    async with ctx.typing():
        r = requests.get("https://whenisthenextmcufilm.com/api")
        raw = r.json()
        du = raw["following_production"]["days_until"]
        over = raw["following_production"]["overview"]
        post = raw["following_production"]["poster_url"]
        dt = raw["following_production"]["release_date"]
        t = raw["following_production"]["title"]
        ty = raw["following_production"]["type"]
        days_until = raw["days_until"]
        overview = raw["overview"]
        poster_url = raw["poster_url"]
        release_date = raw["release_date"]
        title = raw["title"]
        type = raw["type"]

        embed=discord.Embed(title="When is the next MCU film?", colour=ctx.author.colour, url="https://whenisthenextmcufilm.com/", timestamp=datetime.now())
        embed.set_footer(text="Made with ❤️ by qing")
        embed.add_field(name="Title:", value=title, inline=False)
        embed.add_field(name="Release date:", value=f"{release_date} ({days_until} days more)", inline=True)
        embed.add_field(name="Production type:", value=type, inline=True)
        embed.add_field(name="Overview:", value=overview, inline=False)
        embed.add_field(name="What's afterwards?", value=f"{t} ({du} days more)",inline=False)
        embed.set_image(url=poster_url)
        await ctx.reply(embed=embed)

@bot.command()
async def nitro(ctx):
    async with ctx.typing():
        chars = list(string.ascii_lowercase)+list(string.ascii_uppercase)+list(string.digits)
        amt = int(1)
        main = "https://discord.gift/"
        for i in range(amt):
            ending = ""
            for i in range(random.randint(6,16)):
                ending += random.choice(chars)
            await ctx.reply(main+ending)

@bot.command(aliases=["shrink"])
async def shorten(ctx, link = None):
    async with ctx.typing():
        if link == None:
            link = "https://qingbotcommand.netlify.app/"
        s = pyshorteners.Shortener(api_key=bitlyapikey)
        output = s.bitly.short(link)
        await ctx.reply(f"Your shorten link is {output} | It has been used for {s.bitly.total_clicks(output)} times")            

@bot.command()
async def expand(ctx, link = None):
    async with ctx.typing():
        if link == None:
            link = "https://bit.ly/3CrTREY"
        s = urlexpander.expand(link)
        await ctx.reply(f"Your expanded link is {s}")

@bot.command()
async def anime(ctx, namelist = None):
    async with ctx.typing():
        if namelist == "list":
            await ctx.reply("waifu, neko, shinobu, megumin, bully, cuddle, cry, hug, awoo, kiss, lick, pat, smug, bonk, yeet, blush, smile, wave, highfive, handhold, nom, bite, glomp, slap, kill, kick, happy, wink, poke, dance, cringe")
        elif namelist == None:
            url = "https://api.waifu.pics/sfw/"
            list = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe"]
            rs = random.choice(list)
            finallink = url+rs
            r = requests.get(finallink)
            sc = r.status_code
            raw = r.json()
            await ctx.reply(raw["url"])
        else:
            url = "https://api.waifu.pics/sfw/"
            finallink = url+namelist
            r = requests.get(finallink)
            sc = r.status_code
            raw = r.json()
            await ctx.reply(raw["url"])

@bot.command(aliases=["wangzhe", "王者荣耀", "王者", "hok", "honorofkings", "honorofking"])
async def wangzherongyao(ctx, agentname = None):
    async with ctx.typing():
        if agentname == None:
            await ctx.reply("Please input a agent name!")
        else:
            msg = await ctx.reply("Updating JSON file...")
            await asyncio.sleep(1.7)
            await msg.edit(content="Loading JSON file...")
            hui = 'https://raw.githubusercontent.com/qing762/arenaofvalorjson/main/herolist.json'
            f = requests.get(hui)
            dt = f.json()
            result = [x for x in dt if x["cname"] == agentname]
            for xy in result:
                e = xy["ename"]
                c = xy["cname"]
                t = xy["title"]
                n = xy["new_type"]
                h = xy["hero_type"]
                sohai = xy["skin_name"]
                m = xy["moss_id"]

            with open('wangzhe.json', encoding='utf-8') as zh:
                data = json.load(zh)
                list = [key["skinname"] for key in data["heroes"] if agentname == key["name"]]
                for key in data["heroes"]:
                    if agentname == key["name"]:
                        abc = key["link"]
                        s = abc.split('/')
                        shabi = s[5]
                for key in data["heroes"]:
                    if agentname == key["name"]:
                        gannineh = key["name"]
                        l = key["link"]
                        codename = key["uid"]
                        t = key["tip"]
                        sd = key["shortdesc"]

                embed=discord.Embed(color=ctx.author.color)
                embed.set_footer(text=f"API by me and it's open source! Check it out in my Github page!")
                embed.add_field(name='Name', value=gannineh)
                embed.add_field(name="Short description", value=sd)
                embed.add_field(name="UID", value=codename)
                embed.add_field(name="Moss ID", value=m)
                embed.add_field(name="Hero code", value=shabi[0:3])
                embed.add_field(name="Hero type", value=h)
                embed.add_field(name="Tips", value=t)
                embed.add_field(name='Skins', value=", ".join(list))
                embed.add_field(name="Url", value=l)
                embed.set_author(name=gannineh, url=l, icon_url=f"https://game.gtimg.cn/images/yxzj/img201606/heroimg/{shabi[0:3]}/{shabi[0:3]}.jpg")
                embed.set_thumbnail(url=f"https://game.gtimg.cn/images/yxzj/img201606/heroimg/{shabi[0:3]}/{shabi[0:3]}-smallskin-2.jpg")
                await msg.edit(content='', embed=embed)

@bot.command()
async def prefix(ctx):
    async with ctx.typing():
        with open("prefixes.json", "r") as f:
            prx = json.loads(f.read())
            p = prx.get(str(ctx.guild.id), '.')
        await ctx.reply(f"My prefix is `{p}` or <@926975122030596196>")

@bot.command()
async def invite(ctx):
    async with ctx.typing():
        embed = discord.Embed(color=ctx.author.color, title="Invitation for the qing Discord bot", description="To support me, kindly head over to the top.gg link and vote the bot. This means a lot to me and I appreciated it!")
        embed.add_field(name="Direct link", value="[CLICK HERE](https://discord.com/api/oauth2/authorize?client_id=926975122030596196&permissions=8&scope=bot)")
        embed.add_field(name="Top.gg link", value="[CLICK HERE](https://top.gg/bot/926975122030596196)")
        embed.set_footer(text="Made with ❤️ by qing")
        await ctx.reply(embed=embed)

@bot.command(aliases=["love"])
async def ship(ctx, user1: discord.User = None, user2: discord.User = None):
    async with ctx.typing():
        if user1 == None:
            await ctx.reply("Please @ a valid discord user (e.g: <@926975122030596196>)")
            return
        elif user2 == None:
            user2 = ctx.author
        try:
            u1 = await bot.fetch_user(user1.id)
            u2 = await bot.fetch_user(user2.id)

            l = f"https://api.popcat.xyz/ship?user1={u1.avatar.url}&user2={u2.avatar.url}"
            await ctx.reply(l)
        except Exception:
            embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
            embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
            embed.set_footer(text="Made with ❤️ by qing")
            await ctx.reply(embed=embed)

@bot.command()
async def biden(ctx, *, text = f"Made with ❤️ by qing"):
    async with ctx.typing():
        s = text.replace(" ", "+")

        l = f'https://api.popcat.xyz/biden?text={s}'
        await ctx.reply(l)

@bot.command(aliases=["wyr"])
async def wouldyourather(ctx):
    async with ctx.typing():
        wyrl = "https://api.popcat.xyz/wyr"
        memel = "https://api.popcat.xyz/meme"
        req = requests.get(wyrl)
        r = req.json()
        q1 = r["ops1"]
        q2 = r["ops2"]
        req1 = requests.get(memel)
        r1 = req1.json()
        pic = r1["image"]

        embed = discord.Embed(colour = ctx.author.color)
        embed.set_image(url=pic)
        embed.add_field(name="Would you rather...", value=q1, inline=True)
        embed.add_field(name="or", value=q2, inline=True)
        embed.set_footer(text="Made with ❤️ by qing")
        await ctx.reply(embed=embed)

@bot.command(aliases = ["8ball"])
async def _8ball(ctx, question = None):
    if question == None:
        await ctx.reply("Please enter a valid question!")
    else:
        r = requests.get("https://api.popcat.xyz/8ball")
        raw = r.json()
        await ctx.reply(raw["answer"])

@bot.command(aliases=["mc"])
async def minecraft(ctx, username=None):
    async with ctx.typing():
        if username == None:
            await ctx.reply("Please enter a valid Minecraft username!")
            return
        else:
            username == username

        try:
            msg = await ctx.reply("Please wait...")
            await msg.edit(content=f"Fetching game information with the name {username}")
            r = requests.get(f'https://api.ashcon.app/mojang/v2/user/{username}')
            raw = r.json()
            uid = raw["uuid"]
            uuid = uid.replace("-", "")
            finalname = raw["username"]
            await msg.edit(content=f"Fetching {finalname}'s skin")
            sg = skingrabber()

            hy = asyncpixel.Hypixel(hypixelapi)

            await msg.edit(content=f"Fetching Hypixel general information with the name {finalname}")
            embed=discord.Embed(colour=ctx.author.colour, timestamp=datetime.now())
            embed.add_field(name="Name", value=finalname)
            embed.add_field(name="UUID", value=uid)
            embed.add_field(name="UUID (without dash)", value=uuid)
            embed.add_field(name="Created at", value=raw["created_at"] if raw["created_at"] is not None else 'N/A')
            embed.add_field(name="Hypixel level", value=(await hy.player(uuid)).level)
            embed.add_field(name="Hypixel karma", value=(await hy.player(uuid)).karma)
            embed.add_field(name="Hypixel rank", value=(await hy.player(uuid)).rank if (await hy.player(uuid)).rank is not None else 'N/A')
            embed.add_field(name="Hypixel achievement point", value=(await hy.player(uuid)).achievement_points)
            await msg.edit(content=f"Fetching Hypixel bedwars information with the name {finalname}")
            embed.add_field(name="Hypixel bedwars EXP | kills/wins/losses", value=f"{(await hy.player(uuid)).stats.bedwars.experience} | {(await hy.player(uuid)).stats.bedwars.kills}/{(await hy.player(uuid)).stats.bedwars.wins}/{(await hy.player(uuid)).stats.bedwars.losses}")
            await msg.edit(content=f"Fetching Hypixel skywars information with the name {finalname}")
            embed.add_field(name="Hypixel skywars kills/wins/losses", value=f"{(await hy.player(uuid)).stats.skywars.kills}/{(await hy.player(uuid)).stats.skywars.wins}/{(await hy.player(uuid)).stats.skywars.losses}")
            await msg.edit(content=f"Fetching Hypixel duels information with the name {finalname}")
            embed.add_field(name="Hypixel duels damage dealt/wins/losses", value=f"{(await hy.player(uuid)).stats.duels.damage_dealt}/{(await hy.player(uuid)).stats.duels.wins}/{(await hy.player(uuid)).stats.duels.losses}")
            await msg.edit(content=f"Fetching Hypixel build battle information with the name {finalname}")
            embed.add_field(name="Hypixel build battle score/games played/coins", value=f"{(await hy.player(uuid)).stats.build_battle.score} | {(await hy.player(uuid)).stats.build_battle.games_played}/{(await hy.player(uuid)).stats.build_battle.coins}")
            await msg.edit(content=f"Fetching Hypixel the pit information with the name {finalname}")
            embed.add_field(name="Hypixel the pit kills/wins/coins", value=f"{(await hy.player(uuid)).stats.pit.total_kills}/{(await hy.player(uuid)).stats.pit.total_wins}/{(await hy.player(uuid)).stats.pit.coins}")
            await msg.edit(content=f"Fetching Hypixel paintball information with the name {finalname}")
            embed.add_field(name="Hypixel paintball shots fired/wins/deaths", value=f"{(await hy.player(uuid)).stats.paintball.shots_fired}/{(await hy.player(uuid)).stats.paintball.wins}/{(await hy.player(uuid)).stats.paintball.deaths}")
            await msg.edit(content=f"Fetching Hypixel TNT games information with the name {finalname}")
            embed.add_field(name="Hypixel TNT games wins/deaths", value=f"{(await hy.player(uuid)).stats.tnt_games.wins}/{(await hy.player(uuid)).stats.tnt_games.deaths}")
            embed.set_image(url=sg.get_skin_rendered(user=username))
            embed.set_thumbnail(url=f"https://cravatar.eu/renders/head/{uid}")
            embed.set_author(name=f"Profile of {finalname}", url=f"https://namemc.com/profile/{finalname}.1/", icon_url=f"https://crafatar.com/avatars/{uid}")
            embed.set_footer(text="Made with ❤️ by qing")

            await msg.edit(content='', embed=embed)
            await hy.close()
        except Exception:
            await msg.edit(content=f"`{username}` not found!")

@bot.command()
async def unforgivable(ctx, text = None):
    if text == None:
        await ctx.reply("Please enter a valid text!")
    else:
        l = f'https://api.popcat.xyz/unforgivable?text={text}'
        await ctx.reply(l)

@bot.command(aliases=["botbug", "bugs", "helpthereisabug"])
async def bug(ctx):
    async with ctx.typing():
        embed = discord.Embed(title="So you found a bug...", color=ctx.author.color, timestamp=datetime.now())
        embed.add_field(name="Please DM me by clicking the hyperlink", value="[CLICK HERE](https://discord.com/users/635765555277725696)")
        embed.set_footer(text="Made with ❤️ by qing")
    await ctx.reply(embed=embed)

@bot.command()
async def showerthoughts(ctx):
    async with ctx.typing():
        l = 'https://api.popcat.xyz/showerthoughts'
        req = requests.get(l)
        r = req.json()
        text = r["result"]
        up = r["upvotes"]
        aut = r["author"]
        
        embed = discord.Embed(title="Shower thoughts...", color=ctx.author.color, description=text)
        embed.add_field(name="Author", value=aut)
        embed.add_field(name="Upvotes", value=up)
    await ctx.reply(embed=embed)

@bot.command(aliases=["pickup"])
async def pickuplines(ctx):
    async with ctx.typing():
        l = 'https://api.popcat.xyz/pickuplines'
        r = requests.get(l)
        line = r.json()["pickupline"]
        await ctx.reply(line)

@bot.command(aliases=["ttm", "textmorse"])
async def texttomorse(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please enter a valid text!")
        else:
            ft = text.replace(" ", "%20")
            l = f'https://api.popcat.xyz/texttomorse?text={ft}'
            req = requests.get(l)
            r = req.json()["morse"]
            await ctx.reply(r)

@bot.command()
async def oogway(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please enter a valid text!")
        else:
            ft = text.replace(" ", "+")
            l = f'https://api.popcat.xyz/oogway?text={ft}'
            await ctx.reply(l)

@bot.command()
async def caution(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please enter a valid text!")
        else:
            ft = text.replace(" ", "+")
            l = f'https://api.popcat.xyz/caution?text={ft}'
            await ctx.reply(l)

@bot.command(aliases=["decodeb", "db", "binarydecode"])
async def decodebinary(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Your binary integer cannot be blank!")
        else:
            try:
                l = f'https://api.popcat.xyz/decode?binary={text}'
                req = requests.get(l)
                r = req.json()["text"]
                await ctx.reply(r)
            except Exception as e:
                await ctx.reply("Please enter a valid binary integer!")

@bot.command(aliases=["encodeb", "eb", "binaryencode"])
async def encodebinary(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Your text cannot be blank!")
        else:
            ft = text.replace(" ", "+")
            try:
                l = f'https://api.popcat.xyz/encode?text={ft}'
                req = requests.get(l)
                r = req.json()["binary"]
                await ctx.reply(r)
            except Exception as e:
                await ctx.reply("Please enter a valid text!")

@bot.command()
async def quote(ctx):
    async with ctx.typing():
        req = requests.get("https://api.popcat.xyz/quote")
        r = req.json()
        q = r["quote"]
        u = r["upvotes"]

        embed = discord.Embed(color=ctx.author.color, title="Random quotes", description=q)
        embed.add_field(name="Upvotes", value=u)
        embed.set_footer(text="Made with ❤️ by qing")
        await ctx.reply(embed=embed)

@bot.command()
async def wanted(ctx, user: discord.User | str = None):
    async with ctx.typing():
        if isinstance(user, discord.User) or user == None:
            if user == None:
                user = ctx.author
            else:
                user = user
            try:
                pfp = user.display_avatar
                l = f"https://api.popcat.xyz/wanted?image={pfp}"
                await ctx.reply(l)
            except AttributeError:
                await ctx.reply("User not found!")
        elif isinstance(user, str) and user == "help":
            await ctx.reply("The bot will read the displayed avatar of the user for this server if you mention the user. For his/hers normal avatar, please use his/hers discord account ID instead.")
        else:
            return

@bot.command(aliases=["car"])
async def carpic(ctx):
    async with ctx.typing():
        l = 'https://api.popcat.xyz/car'
        req = requests.get(l)
        r = req.json()
        img = r["image"]
        t = r["title"]

        embed=discord.Embed(color=ctx.author.color, description=t)
        embed.set_image(url=img)
        await ctx.reply(embed=embed)

@bot.command()
async def jail(ctx, user: discord.User | str = None):
    async with ctx.typing():
        if isinstance(user, discord.User) or user == None:
            if user == None:
                user = ctx.author
            else:
                user = user
            try:
                pfp = user.display_avatar
                l = f"https://api.popcat.xyz/jail?image={pfp}"
                await ctx.reply(l)
            except AttributeError:
                await ctx.reply("User not found!")
        elif isinstance(user, str) and user == "help":
            await ctx.reply("The bot will read the displayed avatar of the user for this server if you mention the user. For his/hers normal avatar, please use his/hers discord account ID instead.")
        else:
            return

@bot.command(aliases=["emo"])
async def sadcat(ctx, *, text = None):
    if text == None:
        await ctx.reply("Please enter a valid text!")
    else:
        ft = text.replace(" ", "+")
        await ctx.reply(f"https://api.popcat.xyz/sadcat?text={ft}")

@bot.command()
async def chat(ctx, *, q=None):
    if q == None:
        await ctx.reply("Please enter a valid text!")
    else:
        ft = q.replace(" ", "+")
        l = f'https://api.popcat.xyz/chatbot?msg={ft}&owner=qing&botname=qing+Bot'
        req = requests.get(l)
        r = req.json()["response"]
        await ctx.reply(r)

@bot.command(aliases=["www"])
async def whowouldwin(ctx, user1: discord.User = None, user2: discord.User = None):
    async with ctx.typing():
        if user1 == None:
            await ctx.reply("Please @ a valid discord user (e.g: <@926975122030596196>")
        elif user2 == None:
            user2 = ctx.author
        try:
            u1 = await bot.fetch_user(user1.id)
            u2 = await bot.fetch_user(user2.id)

            l = f"https://api.popcat.xyz/whowouldwin?image1={u1.display_avatar.url}&image2={u2.display_avatar.url}"
            await ctx.reply(l)
        except Exception:
            embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
            embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
            embed.set_footer(text="Made with ❤️ by qing")
            await ctx.reply(embed=embed)

@bot.command()
async def gun(ctx, user: discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        else:
            user = user
        
        try:
            l = f"https://api.popcat.xyz/gun?image={user.display_avatar}"
            await ctx.reply(l)
        except Exception:
            await ctx.reply("An error occured! Please check if it is a valid user!")

@bot.command()
async def reverse(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please enter a valid text!")
        else:
            ft = text.replace(" ", "+")
            l = f'https://api.bananonz.dev/reverse?text={ft}'
            req = requests.get(l)
            r = req.json()
            reverse = r["reverse"]
            await ctx.reply(reverse)

@bot.command()
async def ad(ctx, user: discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        else:
            user = user

        try:
            l = f'https://api.popcat.xyz/ad?image={user.display_avatar}'
            await ctx.reply(l)
        except Exception as e:
            await ctx.reply("An error occured! Please check if it is a valid user!")

@bot.command()
async def blur(ctx, user: discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        else:
            user = user

        try:
            l = f'https://api.popcat.xyz/blur?image={user.display_avatar}'
            await ctx.reply(l)
        except Exception as e:
            await ctx.reply("An error occured! Please check if it is a valid user!")

@bot.command()
async def doublestruck(ctx, *, text=None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please enter a valid text!")
        else:
            try:
                ft = text.replace(" ", "+")
                l = f"https://api.popcat.xyz/doublestruck?text={ft}"
                rq = requests.get(l)
                r = rq.json()["text"]
                await ctx.reply(r)
            except Exception as e:
                await ctx.reply("An error occured! Please check if it is a valid text!")

@bot.command(aliases=["movie"])
async def imdb(ctx, *, moviename=None):
    async with ctx.typing():
        if moviename == None:
            await ctx.reply("Please enter a valid movie name!")
        else:
                ft = moviename.replace(" ", "+")
                l = f"https://api.popcat.xyz/imdb?q={ft}"
                rq = requests.get(l)
                r = rq.json()
                sources = [key["source"] for key in r["ratings"]]
                val = [key["value"] for key in r["ratings"]]
                name = r["title"]
                y = r["year"]
                yeardat = r["_yearData"]
                rate = r["rated"]
                release = r["released"]
                t = r["runtime"]
                genre = r["genres"]
                direct = r["director"]
                write = r["writer"]
                act = r["actors"]
                p = r["plot"]
                lan = r["languages"]
                coun = r["country"]
                a = r["awards"]
                post = r["poster"]
                meta = r["metascore"]
                rati = r["rating"]
                vote = r["votes"]
                imd = r["imdbid"]
                t = r["type"]
                d = r["dvd"]
                box = r["boxoffice"]
                product = r["production"]
                web = r["website"]
                nama = r["name"]
                series = r["series"]
                imdblink = r["imdburl"]

                timereal = aniso8601.parse_datetime(release)
                dv = aniso8601.parse_datetime(d)

                timereleased = str(timereal).replace("+", ".")
                dvd = str(dv).replace("+", " ")

                embed = discord.Embed(color=ctx.author.color, title=nama, description=p, url=imdblink)
                embed.set_image(url=post)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.add_field(name="Year released", value=y)
                embed.add_field(name="Year data stored", value=yeardat)
                embed.add_field(name="Rated", value=rate)
                embed.add_field(name="Type", value=t)
                embed.add_field(name="Series?", value="No" if series == "false" else f"Yes")
                embed.add_field(name="Released on", value=timereleased)
                embed.add_field(name="Run time", value=t)
                embed.add_field(name="Genres", value=genre)
                embed.add_field(name="Directed by:", value=direct)
                embed.add_field(name="Writed by:", value=write)
                embed.add_field(name="Acted by:", value=act)
                embed.add_field(name="Languages available", value=lan)
                embed.add_field(name="Country", value=coun)
                embed.add_field(name="Won awards", value=a)
                embed.add_field(name="Metascore", value=meta)
                embed.add_field(name="Ratings", value=rati)
                embed.add_field(name="Votes", value=vote)
                embed.add_field(name="IMDB ID", value=imd)
                embed.add_field(name="DVD released", value=dvd)
                embed.add_field(name="Box office earned", value=box)
                embed.add_field(name="Production", value=product)
                embed.add_field(name="Website", value=web if web == "N/A" else f"[CLICK ME]({web})")
                await ctx.reply(embed=embed)

@bot.command()
async def pat(ctx, user : discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        else:
            user = user

        try:
            l = f"https://api.bananonz.dev/pet?image={user.display_avatar}"
            res = requests.get(l)
            open("pat.gif", "wb").write(res.content)
            await ctx.reply(file = discord.File("pat.gif"))
        except Exception as e:
            await ctx.reply("An error occured! Please check your input!")

@bot.command()
async def pikachu(ctx, *, text = None):
    async with ctx.typing():
        if text == None:
            await ctx.reply("Please input a valid text!")
        else:
            try:
                ft = text.replace(" ", "+")
                l = f"https://api.popcat.xyz/pikachu?text={ft}"
                await ctx.reply(l)
            except Exception as e:
                await ctx.reply("An error occured! Please check your input!")
            except Exception(commands.errors.UserNotFound) as f:
                await ctx.reply("An error occured! Please check your input!")

@bot.command()
async def invert(ctx, *, user : discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        else:
            user = user
            
        try:
            l = f"https://api.popcat.xyz/invert?image={user.display_avatar}"
            await ctx.reply(l)
        except Exception as e:
            await ctx.reply("An error occured! Please check your input!")

@bot.command(aliases=["pt", "periodict", "ptable"])
async def periodictable(ctx, *, element = None):
    async with ctx.typing():
        if element == None:
            await ctx.reply("Please input a valid element!")
        else:
            try:
                element = element
                finalelement = element.replace(" ", "+")
                l = f"https://api.popcat.xyz/periodic-table?element={finalelement}"
                req = requests.get(l)
                r = req.json()
                nama = r["name"]
                symbol = r["symbol"]
                atomnum = r["atomic_number"]
                atommass = r["atomic_mass"]
                per = r["period"]
                ph = r["phase"]
                discover = r["discovered_by"]
                sum = r["summary"]
                i = r["image"]

                embed = discord.Embed(color = ctx.author.color, title=nama, description=sum)
                embed.set_thumbnail(url=i)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.add_field(name="Name", value=nama)
                embed.add_field(name="Symbol", value=symbol)
                embed.add_field(name="Discovered by", value=discover)
                embed.add_field(name="Atomic number", value=atomnum)
                embed.add_field(name="Atomic mass", value=atommass)
                embed.add_field(name="Period", value=per)
                embed.add_field(name="Phase", value=ph)

                await ctx.reply(embed=embed)

            except Exception as e:
                await ctx.reply("An error occured! Please try checking your value if it's a valid element!")

@bot.command(aliases=["colour"])
async def color(ctx, color = None):
    async with ctx.typing():
        if color == None:
            await ctx.reply("Please enter a valid hex code")
        elif color == "random":
            try:
                url = "https://api.popcat.xyz/randomcolor"
                reqs = requests.get(url)
                raw = reqs.json()["hex"]
                l = f"https://api.popcat.xyz/color/{raw}"
                req = requests.get(l)
                r = req.json()
                hex = r["hex"]
                name = r["name"]
                rgb = r["rgb"]
                i = r["color_image"]
                brightened = r["brightened"]

                embed = discord.Embed(color=ctx.author.color, title=f"Information for {name}")
                embed.set_thumbnail(url=i)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.add_field(name="Name", value=name)
                embed.add_field(name="Hex code", value=hex)
                embed.add_field(name="RGB", value=rgb)
                embed.add_field(name="Brightened", value=brightened)
                await ctx.reply(embed=embed)

            except Exception as e:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        else:
            try:
                l = f"https://api.popcat.xyz/color/{color}"
                req = requests.get(l)
                r = req.json()
                hex = r["hex"]
                name = r["name"]
                rgb = r["rgb"]
                i = r["color_image"]
                brightened = r["brightened"]

                embed = discord.Embed(color=ctx.author.color, title=f"Information for {name}")
                embed.set_thumbnail(url=i)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.add_field(name="Name", value=name)
                embed.add_field(name="Hex code", value=hex)
                embed.add_field(name="RGB", value=rgb)
                embed.add_field(name="Brightened", value=brightened)
                await ctx.reply(embed=embed)

            except Exception as e:
                await ctx.reply("An error occured! Please check your input if it is a valid hex colour(color) code!")

@bot.command(aliases=["reddit"])
async def subreddit(ctx, *, subreddit = None):
    async with ctx.typing():
        if subreddit == None:
            await ctx.reply("Please input a valid subreddit name")
        else:
            try:
                l = f"https://api.popcat.xyz/subreddit/{subreddit}"
                req = requests.get(l)
                r = req.json()
                name = r["name"]
                title = r["title"]
                activeuser = r["active_users"]
                member = r["members"]
                description = r["description"]
                icon = r["icon"]
                banner = r["banner"]
                allowvid = r["allow_videos"]
                allowimg = r["allow_images"]
                plus18 = r["over_18"]
                url = r["url"]

                embed = discord.Embed(color=ctx.author.color, title=f"Information of subreddit {name}", url=url, description=description)
                
                if bool(banner) is not False:
                    embed.set_image(url=banner)
                elif icon != "":
                    embed.set_thumbnail(url=icon)
                else:
                    pass

                embed.set_footer(text="Made with ❤️ by qing")
                embed.add_field(name="Name", value=name)
                embed.add_field(name="Title", value=title)
                embed.add_field(name="Active users", value=activeuser)
                embed.add_field(name="Total members", value=member)
                embed.add_field(name="Videos allowed?", value=allowvid)
                embed.add_field(name="Images allowed?", value=allowimg)
                embed.add_field(name="18+?", value=plus18)
                await ctx.reply(embed=embed)
            except Exception as e:
                await ctx.reply("An error occured! Please check your input if it is a valid subreddit name!")

@bot.command(aliases=["grayscale"])
async def greyscale(ctx, user : discord.User = None):
    async with ctx.typing():
        if user == None:
            user = ctx.author
        else:
            user = user

        try:
            l = f"https://api.popcat.xyz/greyscale?image={user.display_avatar}"
            await ctx.reply(l)
        except Exception as e:
            embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
            embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
            embed.set_footer(text="Made with ❤️ by qing")
            await ctx.reply(embed=embed)

@bot.command()
async def paper(ctx, version = None):
    async with ctx.typing():
        link = "https://gist.githubusercontent.com/osipxd/6119732e30059241c2192c4a8d2218d9/raw/71d49e03a3711ab5e192e99ea9a820508d21079f/paper-versions.json"
        req = requests.get(link)
        r = req.json()
        latest = r["latest"]
        i = r["versions"]
        newest = i[f"{latest}"]
        one192 = i["1.19.2"]
        one191 = i["1.19.1"]           
        one19 = i["1.19"]
        one182 = i["1.18.2"]
        one181 = i["1.18.1"]
        one18 = i["1.18"]
        one171 = i["1.17.1"]
        one17 = i["1.17"]
        one165 = i["1.16.5"]
        one164 = i["1.16.4"]
        one163 = i["1.16.3"]
        one162 = i["1.16.2"]
        one161 = i["1.16.1"]
        one152 = i["1.15.2"]
        one144 = i["1.14.4"]
        one132 = i["1.13.2"]
        one122 = i["1.12.2"]
        one112 = i["1.11.2"]
        one102 = i["1.10.2"]
        onenine4 = i["1.9.4"]
        oneeight8 = i["1.8.8"]

        if version == None:
            try:
                embed = discord.Embed(color=ctx.author.color, title="Paper versions downloads")
                embed.add_field(name=f"Latest ({latest}", value=f"[CLICK HERE TO DOWNLOAD]({newest})")
                embed.add_field(name="1.19.2", value=f"[CLICK HERE TO DOWNLOAD]({one192})")
                embed.add_field(name="1.19.1", value=f"[CLICK HERE TO DOWNLOAD]({one191})")
                embed.add_field(name="1.19", value=f"[CLICK HERE TO DOWNLOAD]({one19})")
                embed.add_field(name="1.18.2", value=f"[CLICK HERE TO DOWNLOAD]({one182})")
                embed.add_field(name="1.18.1", value=f"[CLICK HERE TO DOWNLOAD]({one181})")
                embed.add_field(name="1.18", value=f"[CLICK HERE TO DOWNLOAD]({one18})")
                embed.add_field(name="1.17.1", value=f"[CLICK HERE TO DOWNLOAD]({one171})")
                embed.add_field(name="1.17", value=f"[CLICK HERE TO DOWNLOAD]({one17})")
                embed.add_field(name="1.16.5", value=f"[CLICK HERE TO DOWNLOAD]({one165})")
                embed.add_field(name="1.16.4", value=f"[CLICK HERE TO DOWNLOAD]({one164})")
                embed.add_field(name="1.16.3", value=f"[CLICK HERE TO DOWNLOAD]({one163})")
                embed.add_field(name="1.16.2", value=f"[CLICK HERE TO DOWNLOAD]({one162})")
                embed.add_field(name="1.16.1", value=f"[CLICK HERE TO DOWNLOAD]({one161})")
                embed.add_field(name="1.15.2", value=f"[CLICK HERE TO DOWNLOAD]({one152})")
                embed.add_field(name="1.14.4", value=f"[CLICK HERE TO DOWNLOAD]({one144})")
                embed.add_field(name="1.13.2", value=f"[CLICK HERE TO DOWNLOAD]({one132})")
                embed.add_field(name="1.12.2", value=f"[CLICK HERE TO DOWNLOAD]({one122})")
                embed.add_field(name="1.11.2", value=f"[CLICK HERE TO DOWNLOAD]({one112})")
                embed.add_field(name="1.10.2", value=f"[CLICK HERE TO DOWNLOAD]({one102})")
                embed.add_field(name="1.9.4", value=f"[CLICK HERE TO DOWNLOAD]({onenine4})")
                embed.add_field(name="1.8.8", value=f"[CLICK HERE TO DOWNLOAD]({oneeight8})")
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "latest":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{latest}` version", url=newest)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.19.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one192)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.19.1":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one191)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.19":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one19)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.18.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one182)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.18.1":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one181)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.18":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one18)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.17.1":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one171)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.17":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one17)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.16.5":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one165)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.16.4":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one164)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.16.3":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one163)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.16.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one162)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.16.1":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one161)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.15.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one152)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.14.4":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one144)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.13.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one132)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.12.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one122)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.11.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one112)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.10.2":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=one102)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.9.4":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=onenine4)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        elif version == "1.8.8":
            try:
                embed = discord.Embed(color=ctx.author.color, title = f"Click me to download the `{version}` version", url=oneeight8)
                embed.set_footer(text="Made with ❤️ by qing")
                embed.set_image(url="https://papermc.io/images/jumbotron.png")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
                embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)

        else:
            await ctx.reply("Version not found!")

@bot.command(aliases=["profilepicture", "profilepic", "pfp"])
async def avatar(ctx, user : discord.User = None):
        if user == None:
            user = ctx.author
        else:
            user = user

        try:
            await ctx.reply(user.display_avatar)
        except Exception as e:
            embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
            embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
            embed.set_footer(text="Made with ❤️ by qing")
            await ctx.reply(embed=embed)

@bot.command(aliases=["val", "valo"])
async def valorant(ctx, cmdname = None, *, nama = None):
    async with ctx.typing():
        st = ["stats", "account", "stat"]
        ag = ["agent", "hero", "heroes", "agents"]
        if cmdname in st:
            if nama == None:
                await ctx.reply("Please enter a valid VALORANT ign/agent name.")
            else:
                try:
                    nam, tag = nama.split("#")
                    name = nam.replace(" ", "%20")
                except Exception:
                    await ctx.reply("An error occured! Please try checking your name.")
                    return
                
                try:
                    l = f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
                    req = requests.get(l)
                    r = req.json()
                    d = r["data"]
                    puuid = d["puuid"]
                    region = d["region"]
                    acc_lvl = d["account_level"]
                    n = d["name"]
                    tg = d["tag"]
                    widecard = d["card"]["wide"]
                    cardid = d["card"]["id"]
                    rawupdate = d["last_update_raw"]
                    update = d["last_update"]
                    timestamp = f"<t:{rawupdate}:R>"

                    na = n.replace(" ", "%20")
                    link = f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{na}/{tg}"
                    reql = requests.get(link)
                    lr = reql.json()
                    mmrchange = lr["data"]["current_data"]["mmr_change_to_last_game"]
                    currentrank = lr["data"]["current_data"]["currenttierpatched"]
                    currentranknumber = lr["data"]["current_data"]["currenttier"]
                    rankintier = lr["data"]["current_data"]["ranking_in_tier"]
                    gameneedforrank = lr["data"]["current_data"]["games_needed_for_rating"]
                    old = lr["data"]["current_data"]["old"]
                    elo = lr["data"]["current_data"]["elo"]
                    currentseasonwins = lr["data"]["by_season"]["e5a3"]["wins"]
                    currentseasongames = lr["data"]["by_season"]["e5a3"]["number_of_games"]
                    img = lr["data"]["current_data"]["images"]["large"]

                    embed = discord.Embed(color=ctx.author.color, title=f"Valorant information for {n}#{tg}", description=puuid)
                    embed.set_image(url=widecard)
                    embed.set_thumbnail(url=img)
                    embed.add_field(name="Name", value=n)
                    embed.add_field(name="Tag", value=tg)
                    embed.add_field(name="Region", value=region)
                    embed.add_field(name="Account level", value=acc_lvl)
                    embed.add_field(name="Account rank", value=f"{currentrank} ({'#N/A' if currentrank != 'Radiant' else f'#{rankintier}'})")
                    embed.add_field(name="Acount of games played in current act", value=f"{currentseasongames} games")
                    embed.add_field(name="Amount of games left for ranking", value=f"{gameneedforrank} games")
                    embed.add_field(name="Current act wins", value=f"Won {currentseasonwins} games")
                    embed.add_field(name="MMR changes to last game", value=f"{mmrchange} MMR")
                    embed.add_field(name="Elo", value=elo)
                    embed.add_field(name="Last updated", value=timestamp)
                    embed.add_field(name="Old data?", value=f"Yes" if old == "True" else "No")
                    embed.set_footer(text="Made with ❤️ by qing")
                    await ctx.reply(embed=embed)
                except Exception:
                    embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!", description="Please try again. Do note that newer account with low amount of stats will also causes this problem. But if the problem still persists, [please contact the bot owner](https://discord.com/users/635765555277725696)")
                    embed.set_footer(text="Made with ❤️ by qing")
                    await ctx.reply(embed=embed)
        elif cmdname in ag:
            if nama == None:
                await ctx.reply("Please enter a VALORANT agent name!")
            else:
                try:
                    l = "https://valorant-api.com/v1/agents?isPlayableCharacter=true"
                    req = requests.get(l)
                    r = req.json()
                    for x in r["data"]:
                        if str(nama).capitalize() == x["displayName"]:
                            role = x["role"]
                            icon = x["displayIcon"]
                            uuid = x["uuid"]
                            mingzi = x["displayName"]
                            devname = x["developerName"]
                            fullportraitv2 = x["fullPortraitV2"]
                            assetpath = x["assetPath"]
                            isFullPortraitRightFacing = x["isFullPortraitRightFacing"]
                            isPlayableCharacter = x["isPlayableCharacter"]
                            isAvailableForTest = x["isAvailableForTest"]
                            isBaseContent = x["isBaseContent"]
                            rolename = role["displayName"]
                            roleuuid = role["uuid"]

                            for y in x["abilities"]:
                                if y["slot"] == "Ability1":
                                    ming = y["displayName"]
                                elif y["slot"] == "Ability2":
                                    min = y["displayName"]
                                elif y["slot"] == "Grenade":
                                    mi = y["displayName"]
                                elif y["slot"] == "Ultimate":
                                    mingz = y["displayName"]
                            
                            embed = discord.Embed(color=ctx.author.color, title=f"Agent information for {mingzi}", description=assetpath)
                            embed.set_thumbnail(url=icon)
                            embed.set_image(url=fullportraitv2)
                            embed.add_field(name="Display name", value=mingzi)
                            embed.add_field(name="Developer name", value=devname)
                            embed.add_field(name="Role", value=rolename)
                            embed.add_field(name="-----------------------------------------------", value="**-----------------------------------------------**", inline=False)
                            embed.add_field(name="Ability 1", value=mi)
                            embed.add_field(name="Ability 2", value=ming)
                            embed.add_field(name="Ability 3 (aka Grenade)", value=min)
                            embed.add_field(name="Ability 4 (aka Ultimate)", value=mingz)
                            embed.add_field(name="-----------------------------------------------", value="**-----------------------------------------------**", inline=False)
                            embed.add_field(name="Is full character portrait right facing?", value="Yes" if isFullPortraitRightFacing == "true" else "No", inline=False)
                            embed.add_field(name="Is it a playable character?", value="Yes" if isPlayableCharacter == "true" else "No", inline=False)
                            embed.add_field(name="Is it available for testing?", value="Yes" if isAvailableForTest == "true" else "No", inline=False)
                            embed.add_field(name="Is it a base content?", value="Yes" if isBaseContent == "true" else "No", inline=False)
                            embed.set_footer(text="Made with ❤️ by qing")
                            await ctx.reply(embed=embed)
                except Exception:
                    embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!", description="Please try again. Do note that newer account with low amount of stats will also causes this problem. But if the problem still persists, [please contact the bot owner](https://discord.com/users/635765555277725696)")
                    embed.set_footer(text="Made with ❤️ by qing")
                    await ctx.reply(embed=embed)
        elif cmdname == "list":
            try:
                embed = discord.Embed(color=ctx.author.color, title="Commands list for `.valorant`")
                embed.add_field(name="agent `{agent name}`", value="Information about specific agent in the game VALORANT.", inline=False)
                embed.add_field(name="stats `{ign}`", value="Account information for the game VALORANT", inline=False)
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)
            except Exception:
                embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!", description="Please try again. Do note that newer account with low amount of stats will also causes this problem. But if the problem still persists, [please contact the bot owner](https://discord.com/users/635765555277725696)")
                embed.set_footer(text="Made with ❤️ by qing")
                await ctx.reply(embed=embed)
        else:
            await ctx.reply("Please enter a valid command name.")

@bot.command()
@commands.is_owner()
async def testembed(ctx):
    async with ctx.typing():
        embed = discord.Embed(color=ctx.author.color, title="This is a test embed", description="This is the description of the test embed")
        embed.add_field(name="Name", value="value1 \n value2")
        embed.set_footer(text="Made with ❤️ by qing")
        await ctx.reply(embed=embed)
  
@bot.command(aliases=["futsal", "football", "fifaworldcup2022", "fwc2022", "fwc"])
async def fifaworldcup(ctx, cmdname = None, *, teamname = None):
    async with ctx.typing():
        email = os.getenv('FIFAEMAIL')
        password = os.getenv('FIFAPASSWORD')
        json_data = {
            'email': email,
            'password': password,
        }

        response = requests.post('http://api.cup2022.ir/api/v1/user/login', json=json_data)
        tok = response.json()

        headers = {
            'Authorization': tok['data']['token'],
            'Content-Type': 'application/json',
            }

        if cmdname == None:
            await ctx.reply("Please pass in a valid football command name!")
        elif cmdname == "team":
            if teamname != None:
                try:
                    response = requests.get('http://api.cup2022.ir/api/v1/team', headers=headers)
                    ts = requests.get('http://api.cup2022.ir/api/v1/standings', headers=headers)
                    s = ts.json() 
                    r = response.json()

                    tmname = teamname[0].upper() + teamname[1:]
                    for xy in r["data"]:
                        if xy["name_en"] == tmname:
                            _id = xy["_id"]
                            name_en = xy["name_en"]
                            name_fa = xy["name_fa"]
                            flag = xy["flag"]
                            fifacode = xy["fifa_code"]
                            iso2 = xy["iso2"]
                            group = xy["groups"]
                            id = xy["id"]

                    for hh in s["data"]:
                        for h in hh["teams"]:
                            if name_en == h["name_en"]:
                                mp = h["mp"]
                                w = h["w"]
                                l = h["l"]
                                pts = h["pts"]
                                gf = h["gf"]
                                ga = h["ga"]
                                d = h["d"]

                    embed = discord.Embed(color = ctx.author.color, title=f"Information about {name_en}", description=_id)
                    embed.set_image(url=flag)
                    embed.add_field(name="ID", value=id)
                    embed.add_field(name="Name (EN)", value=name_en)
                    embed.add_field(name="Name (FA)", value=name_fa)
                    embed.add_field(name="Fifa code", value=fifacode)
                    embed.add_field(name="ISO 2", value=iso2)
                    embed.add_field(name="Group", value=group)
                    embed.add_field(name="Matched played", value=f"{mp} match(es)")
                    embed.add_field(name="Matched won", value=f"{w} match(es)")
                    embed.add_field(name="Matched lost", value=f"{l} match(es)")
                    embed.add_field(name="Matches drawn", value=f"{d} match(es)")
                    embed.add_field(name="Point / score", value=f"{pts} point(s)")
                    embed.add_field(name="Goals for", value=f"{gf} goal(s)")
                    embed.add_field(name="Goals againts", value=f"{w} goal(s)")
                    embed.add_field(name="Goals difference", value=f"{w} goal(s)")
                    embed.set_footer(text="Made with ❤️ by qing")
                    await ctx.reply(embed=embed)

                except ValueError:
                    embed = discord.Embed(color=ctx.author.color, description="Please try again. This error occurs when the API refreshes. If it continuously happen, please [contact the bot owner.](https://discord.com/users/635765555277725696)")
                    await ctx.reply(embed=embed)

                except Exception:
                    await ctx.reply("Uh-oh! An error occured! Maybe it's not qualified for `2022 FIFA World Cup`? Try double checking your input.")
                
            else:
                await ctx.reply("Please pass in a valid country name!")
        else:
            await ctx.reply(f"Command `{cmdname}` not found!")

@bot.command(aliases=['cp'])
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix = None):
    async with ctx.typing():
        if prefix == None:
            await ctx.reply("Please pass in a valid prefix!")
        else:
            try:
                with open('prefixes.json', 'r') as f:
                    prefixes = json.load(f)

                prefixes[str(ctx.guild.id)] = prefix
            
                with open('prefixes.json', 'w') as f:
                    json.dump(prefixes, f, indent=4)
            
                await ctx.reply(f'The server prefix had changed to: {prefix}')
            except commands.MissingPermissions:
                await ctx.reply("You dont have permission to do that! Please contact the server administrator!")

@bot.command(aliases=["githubrepo", "repo", "githubrepository"])
async def repository(ctx):
    embed = discord.Embed(color=ctx.author.color, description="[Consider leave a star on my github repo!](https://github.com/qing762/qingbot)")
    embed.set_footer(text="Made with ❤️ by qing")
    await ctx.reply(embed=embed)

@bot.command()
async def help(ctx):
    async with ctx.typing():
        # list = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug", "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe"]
        url = "https://api.popcat.xyz/meme"
        # rc = random.choice(list)
        # finallink = url+rc
        r = requests.get(url)
        raw = r.json()
        embed=discord.Embed(colour=ctx.author.colour, description="`{}` = Required argument | `()` = Optional argument")
        embed.set_author(name= "Commands list and feature for qing Bot (Page 1)", icon_url="https://cdn.discordapp.com/avatars/926975122030596196/ec8d34788d74182533f70f6a56bddca1.png?size=1024")        
        embed.add_field(name="help", value="Shows this message", inline=True)
        embed.add_field(name="bug", value="So you found a bug...")
        embed.add_field(name="repo", value="The github repository link for this open-source bot")
        embed.add_field(name="drip `(@user or <@id>)`", value="Profile picture + black hoodie", inline=True)
        embed.add_field(name="uncover `(@user or <@id>)`", value="Profile picture in a wall", inline=True)
        embed.add_field(name="osuprofile `(name)`", value="Account information for the game osu!", inline=True)
        embed.add_field(name="github `(name)`", value="Account information for the website Github", inline=True)
        embed.add_field(name="serverinfo", value="Shows the information of the current server", inline=True)
        embed.add_field(name="userinfo `(@user or <@id>)`", value="Shows the information of the user", inline=True)
        embed.add_field(name="minecraft `{ign}`", value="Account information for the game Minecraft", inline=True)
        embed.add_field(name="mcskinraw `{ign}`", value="Get raw skin of the Minecraft username", inline=True)
        embed.add_field(name="mcskinrendered `{ign}`", value="Get rendered skin of the Minecraft username", inline=True)
        embed.add_field(name="pi", value="22/7")
        embed.add_field(name="say `{text}`", value="Type anything you want the bot to say")
        embed.add_field(name="ping", value="Simplified version of the deprecated command speedtest")
        embed.add_field(name="whenisthenextmcufilm", value="Marvel film")
        embed.add_field(name="nitro", value="Generate a nitro link")
        embed.add_field(name="shorten `(link)`", value="Shortens a long link", inline=True)
        embed.add_field(name="expand `(link)`", value="Expands a shortened link in case you're afraid of getting rickrolled lmao", inline=True)
        embed.add_field(name="wangzherongyao `{hero name}`", value="Information of specific heroes for the game Honor of Kings", inline=True)

        embed2 = discord.Embed(color = ctx.author.colour, description = "`{}` = Required argument | `()` = Optional argument")
        embed2.set_author(name= "Commands list and feature for qing Bot (Page 2)", icon_url="https://cdn.discordapp.com/avatars/926975122030596196/ec8d34788d74182533f70f6a56bddca1.png?size=1024")
        embed2.add_field(name="prefix", value="Returns the bot prefix", inline=True)
        embed2.add_field(name="invite", value="Invitation link for the bot", inline=True)
        embed2.add_field(name="ship `{@user1} (@user2)`", value=" L O V E ")
        embed2.add_field(name="biden `{text}`", value="Make Biden tweet anything!")
        embed2.add_field(name="wyr", value="Would you rather!")
        embed2.add_field(name="unforgivable `{text}`", value="So you know how some sins are unforgivable?")
        embed2.add_field(name="anime", value="Returns random anime pictures", inline=True)
        embed2.add_field(name="showerthoughts", value="Random shower thoughts")
        embed2.add_field(name="encodebinary `{text}`", value="Encode your text into binary numbers")
        embed2.add_field(name="decodebinary `{binary numbers}`", value="Decode binary numbers into text")
        embed2.add_field(name="oogway `{text}`", value="Create an 'Oogway Quote' meme")
        embed2.add_field(name="caution `{text}`", value="A caution banner that looks real")
        embed2.add_field(name="quote", value="Returns random quote")
        embed2.add_field(name="wanted `(@user or <@id>)`", value="Create a fake wanted poster (`.wanted help` for more)")
        embed2.add_field(name="jail `(@user or <@id>)`", value="Create a fake jail overlay image (`.jail help` for more)")
        embed2.add_field(name="carpic", value="Returns random picture about car")
        embed2.add_field(name="sadcat `{text}`", value="Let the tears release it out")
        embed2.add_field(name="chat `{text}`", value="Chat with the bot! One-time use only for each time you sent the command.")
        embed2.add_field(name="whowouldwin `{@user1} (@user2)`", value="Make a WhoWouldWin meme")
        embed2.add_field(name="gun `(@user or <@id>)`", value="Get a perfect gun overlay on any profile picture")
        embed2.add_field(name="reverse `{text}`", value="Returns text but reversed")
        embed2.add_field(name="ad `(@user or <@id>)`", value="Make someone an ad")
        embed2.add_field(name="blur `(@user or <@id>)`", value="Profile picture, but blured")
        embed2.add_field(name="doublestruck `{text}`", value="Convert your text into the doublestruck font")
        embed2.add_field(name="imdb `{movie name}`", value="Get Tons Of Information On Movies")               
        
        embed3 = discord.Embed(color=ctx.author.color, description = "`{}` = Required argument | `()` = Optional argument")
        embed3.set_footer(text="Made with ❤️ by qing")
        embed3.set_author(name= "Commands list and feature for qing Bot (Page 3)", icon_url="https://cdn.discordapp.com/avatars/926975122030596196/ec8d34788d74182533f70f6a56bddca1.png?size=1024")
        embed3.add_field(name="pat `(@user or <@id>)`", value="Get patted")
        embed3.add_field(name="invert `(@user or <@id>)`", value="Invert the colors of someone profile picture")
        embed3.add_field(name="periodictable `{element name/symbol/number}`", value="Get information about elements in the periodic table")
        embed3.add_field(name="colour(color) `{hex colour(color) code OR 'random'}`", value="Get info on a hex color! Don't know where to start? Try `.colour random` or `.color random`")
        embed3.add_field(name="subreddit `{subreddit}`", value="Get tons of info on a subreddit")
        embed3.add_field(name="greyscale `(@user or <@id>`", value="Make someone's avatar more grey")
        embed3.add_field(name="paper `(version)`", value="Quick links to download PaperMC versions")
        embed3.add_field(name="avatar `(@user or <@id>)`", value="Profile pictures!")
        embed3.add_field(name="valorant `{commandname} {input}`", value="Information of the game VALORANT (For help, `.valorant list`)")
        embed3.add_field(name="fifaworldcup team `{country name}`", value="Information about the 2022 FIFA World Cup")
        embed3.add_field(name="changeprefix `{prefix}`", value="Change the bot prefix for your server!")
        embed3.set_image(url=raw["image"])

        await ctx.reply(embed=embed)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)

bot.run(token)