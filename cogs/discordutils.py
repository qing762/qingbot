import discord
import base64
import datetime
import os
import requests
import json
import asyncio

from discord.ext import commands
from datetime import datetime

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

class DiscordUtils(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("'DiscordUtils' is loaded!")

	#FixME
	@commands.command(pass_context=True, aliases=["user", "userprofile", "userprof", "whois"])
	async def userinfo(self, ctx, user : discord.User = None):
		async with ctx.typing():
			guild = self.bot.get_guild(ctx.guild.id)

			if user == None:
				user = ctx.author
			else:
				user = user

			userid = await self.bot.fetch_user(f"{user.id}")

			createdat = user.created_at
			createdtime = createdat.strftime("%d/%m/%Y %H:%M:%S")

			today = datetime.utcnow()
			now = today.strftime("%d/%m/%Y %H:%M:%S")

			if guild.get_member(int(user.id)) is not None:
				m = await commands.MemberConverter().convert(ctx=ctx, argument=str(user))
				joinedtime = m.joined_at.strftime("%d/%m/%Y %H:%M:%S")
				joingmt = f"{joinedtime} GMT"
				rolelist = []
				for roles in m.roles:
					if roles.name != "@everyone":
						rolelist.append(f"<@&{roles.id}>")
				b = ', '.join(rolelist)

				if m.premium_since != None:
					nitro = m.premium_since.strftime("%d/%m/%Y %H:%M:%S")
					finalnitro = f"{nitro} GMT"
				else:
					finalnitro = 'N/A'

				embed=discord.Embed(colour=user.color)
				embed.add_field(name="Username:", value=f"{user.name}", inline=True)
				embed.add_field(name="Discriminator:", value=f"{user.discriminator}", inline=True)
				embed.add_field(name="Server Username:", value=f"{user.display_name}", inline=True)
				embed.add_field(name="User ID:", value=f"{user.id}", inline=True)
				embed.add_field(name="Is bot?", value=f"{user.bot}", inline=True)
				embed.add_field(name="Status:", value=f"{m.raw_status if m.raw_status is not None else 'N/A'}")
				embed.add_field(name="Presence:", value=f"{str(m.activity.type).split('.')[-1].title() if m.activity is not None else 'N/A'} {m.activity.name if m.activity else ''}")
				embed.add_field(name="Nitro?", value=f"{bool(m.premium_since)}", inline=True)
				embed.add_field(name="Nitro since:", value=f"{finalnitro}")
				embed.add_field(name=f"Roles ({len(rolelist)}):", value=f"".join([b]), inline=False)
				embed.add_field(name="Top role:", value=f"{m.top_role.mention}", inline=True)
				embed.add_field(name="Account created at:", value=f"{createdtime} GMT", inline=True)
				embed.add_field(name="Joined server at:", value=f"{joingmt}", inline=True)
				embed.set_thumbnail(url=user.display_avatar.url)
				embed.set_footer(text="Made with ❤️ by qing")
				embed.set_author(name=f"User information for @{user.name}#{user.discriminator}", icon_url=user.avatar.url)
				embed.set_image(url=userid.banner.url if userid.banner else 'https://qingbotcommand.netlify.app/shabi.webp')
				await ctx.reply(embed=embed)

			else:
				embed = discord.Embed(colour=user.color)
				embed.add_field(name="Username:", value=f"{user.name}", inline=True)
				embed.add_field(name="Discriminator:", value=f"{user.discriminator}", inline=True)
				embed.add_field(name="User ID:", value=f"{user.id}", inline=True)
				embed.add_field(name="Is bot?", value=f"{'Yes' if user.bot == True else 'No'}", inline=True)
				embed.add_field(name="Account created at:", value=f"{createdtime} GMT", inline=True)
				embed.set_thumbnail(url=user.display_avatar.url)
				embed.set_footer(text="Made with ❤️ by qing")
				embed.set_author(name=f"User information for @{user.name}#{user.discriminator}", icon_url=user.avatar.url)
				embed.set_image(url=userid.banner.url if userid.banner else 'https://qingbotcommand.netlify.app/shabi.webp')
				await ctx.reply(embed=embed)

	@commands.command(aliases=["server", "serverprofile", "serverprof", "serverinf"])
	async def serverinfo(self, ctx):
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
			embed.set_footer(text="Made with ❤️ by qing")
			embed.set_thumbnail(url=simple.icon)
			embed.set_author(name=f"Request made by {ctx.author}", icon_url=ctx.author.avatar.url)
			embed.set_image(url=simple.splash)
		await ctx.reply(embed=embed)

	@commands.command()
	async def say(self, ctx, *, message = None):
		async with ctx.typing():
			if message == None:
				await ctx.reply("Please pass in a required argument")
			else:
				await ctx.send(f"{ctx.author.mention} wants to say : ```{message}```")

	@commands.command()
	async def ping(self, ctx):
		resp = await ctx.reply('Pong! Loading...')
		diff = resp.created_at - ctx.message.created_at
		totalms = 1000 * diff.total_seconds()
		emb = discord.Embed()
		emb.title = "Pong!"
		emb.add_field(name="Your message time", value=f"{totalms}ms")
		emb.add_field(name="The API latency", value=f"{(1000 * self.bot.latency):.1f}ms")
		emb.set_footer(text="Made with ❤️ by qing")
		await resp.edit(embed=emb, content="")

	@commands.command()
	async def prefix(self, ctx):
		async with ctx.typing():
			with open("prefixes.json", "r") as f:
				prx = json.loads(f.read())
				p = prx.get(str(ctx.guild.id), '.')
			await ctx.reply(f"My prefix is `{p}` or <@926975122030596196>")

	@commands.command()
	async def invite(self, ctx):
		async with ctx.typing():
			embed = discord.Embed(color=ctx.author.color, title="Invitation for the qing Discord bot", description="To support me, kindly head over to the top.gg link and vote the bot. This means a lot to me and I appreciated it!")
			embed.add_field(name="Direct link", value="[CLICK HERE](https://discord.com/api/oauth2/authorize?client_id=926975122030596196&permissions=8&scope=bot)")
			embed.add_field(name="Top.gg link", value="[CLICK HERE](https://top.gg/bot/926975122030596196)")
			embed.set_footer(text="Made with ❤️ by qing")
			await ctx.reply(embed=embed)

	@commands.command(aliases=["botbug", "bugs", "helpthereisabug"])
	async def bug(self, ctx):
		async with ctx.typing():
			embed = discord.Embed(title="So you found a bug...", color=ctx.author.color, timestamp=datetime.now())
			embed.add_field(name="Please DM me by clicking the hyperlink", value="[CLICK HERE](https://discord.com/users/635765555277725696)")
			embed.set_footer(text="Made with ❤️ by qing")
		await ctx.reply(embed=embed)

	@commands.command(aliases=["profilepicture", "profilepic", "pfp"])
	async def avatar(self, ctx, user : discord.User = None):
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
		
	@commands.command(aliases=['cp'])
	@commands.has_permissions(administrator = True)
	async def changeprefix(self, ctx, prefix = None):
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
				
					await ctx.reply(f'The server prefix had changed to: `{prefix}`')
				except commands.MissingPermissions:
					await ctx.reply("You dont have permission to do that! Please contact the server administrator!")

	@commands.command(aliases=["githubrepo", "repo", "githubrepository"])
	async def repository(self, ctx):
		embed = discord.Embed(color=ctx.author.color, description="[Consider leave a star on my github repo!](https://github.com/qing762/qingbot)")
		embed.set_footer(text="Made with ❤️ by qing")
		await ctx.reply(embed=embed)

	@commands.command()
	async def api(self, ctx):
		async with ctx.typing():
			embed = discord.Embed(color=ctx.author.color, description="API that I uses for this bot!")
			embed.set_footer(text="Made with ❤️ by qing")
			embed.add_field(name="discord.py", value="[CLICK HERE FOR IT'S WEBSITE](https://github.com/Rapptz/discord.py)")
			embed.add_field(name="POP CAT API", value="[CLICK HERE FOR IT'S WEBSITE](https://api.popcat.xyz/) | [CLICK HERE FOR IT'S DISCORD SERVER](https://discord.gg/ds5zYpyt4T)")
			embed.add_field(name="Bananonz API", value="[CLICK HERE FOR IT'S WEBSITE](https://api.bananonz.dev/) | [CLICK HERE FOR IT'S DISCORD SERVER](https://discord.com/invite/eQDtFDnb6x)")
			embed.add_field(name="Hypixel API", value="[CLICK HERE FOR IT'S WEBSITE](https://api.hypixel.net/) | [CLICK HERE FOR IT'S DISCORD SERVER](https://discord.gg/hypixel)")
			embed.add_field(name="osu! API", value="[CLICK HERE FOR IT'S WEBSITE](https://osu.ppy.sh/api) | [CLICK HERE FOR IT'S DISCORD SERVER](https://discord.gg/osu)")
			embed.add_field(name="MCU-Countdown API", value="[CLICK HERE FOR IT'S WEBSITE](https://whenisthenextmcufilm.com/)")
			embed.add_field(name="Waifu PICS API", value="[CLICK HERE FOR IT'S WEBSITE](https://waifu.pics/docs)")
			embed.add_field(name="Minecraft API", value="[CLICK HERE FOR IT'S WEBSITE](https://wiki.vg/Mojang_API)")
			embed.add_field(name="Honor of Kings API", value="[CLICK HERE FOR IT'S WEBSITE](https://github.com/qing762/honor-of-kings-json)")
			embed.add_field(name="Fifa World Cup Qatar 2022 API", value="[CLICK HERE FOR IT'S WEBSITE](https://github.com/raminmr/free-api-worldcup2022)")
			embed.add_field(name="VALORANT-API", value="[CLICK HERE FOR IT'S WEBSITE](https://valorant-api.com/)")
			embed.add_field(name="VALORANT API", value="[CLICK HERE FOR IT'S WEBSITE](https://github.com/Henrik-3/unofficial-valorant-api)")
		await ctx.reply(embed=embed)

	@commands.command()
	async def help_old(self, ctx, page = None):
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
			embed.add_field(name="api", value="API that I uses for this bot")
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
			embed3.add_field(name="pikachu `{text}`", value="Surprised pikachu! :0")
			embed3.add_field(name="jokeoverhead `{@user or <@id>}`", value="[DEPRECATED] This guy doesn't gets any jokes at all lol!")
			embed3.add_field(name="wordle", value="[DEPRECATED] Wordle solutions") 
			embed3.add_field(name="patchnotes", value="[DEPRECATED] Patch notes for each updates!")
			embed3.add_field(name="colourify `{@user}`", value="[DEPRECATED] Overlay a variety of colors on your avatar")
			embed3.add_field(name="speedtest", value="[DEPRECATED] Test the current internet speed between you and the bot.")
			embed3.add_field(name="wangzherongyao_old `{hero name}`", value="[DEPRECATED] Information of specific heroes for the game Honor of Kings (Do note that new heroes might not be included in this command)", inline=True)
			embed3.set_image(url=raw["image"])

			if page == None:
				await ctx.reply(embed=embed)
				await ctx.send(embed=embed2)
				await ctx.send(embed=embed3)
				await ctx.reply("This command is planned to be deprecated on 1/1/2023. Please use `.help` instead.")
			elif page == "1":
				await ctx.reply(embed = embed)
				await ctx.reply("This command is planned to be deprecated on 1/1/2023. Please use `.help` instead.")
			elif page == "2":
				await ctx.reply(embed=embed2)
				await ctx.reply("This command is planned to be deprecated on 1/1/2023. Please use `.help` instead.")
			elif page == "3":
				await ctx.reply(embed=embed3)
				await ctx.reply("This command is planned to be deprecated on 1/1/2023. Please use `.help` instead.")
			else:
				await ctx.reply("Page number not found!")
				await ctx.reply("This command is planned to be deprecated on 1/1/2023. Please use `.help` instead.")

	@commands.command()
	@commands.is_owner()
	async def help(self, ctx):
		async with ctx.typing():
			current = 0
			reactions = ['⏪', '⬅️', '🚫', '➡️', '⏩']

			embed = discord.Embed(color=ctx.author.color, description="<@926975122030596196> is a Discord bot written by [qing762](https://discord.com/users/635765555277725696) with Python")
			embed.add_field(name="Stucked with the commands?", value="Run `.help` followed by the command name as the argument.", inline=False)
			embed.add_field(name="Don't know where to start?", value="React to this message to start.", inline=False)
			embed.set_footer(text="Made with ❤️ by qing")

			embed2 = discord.Embed(color=ctx.author.color, title="Commands for category 'Extensions'", description="This category is owner-only for commands maintainance purposes and cannot be used by other people.")
			embed2.add_field(name="extensionlist", value="Output the list of extensions/categories.\n```Arguments: None```", inline=False)
			embed2.add_field(name="load", value="Loads the specific extension/category.\n```Arguments: extension```", inline=False)
			embed2.add_field(name="unload", value="Unloads the specific extension/category.\n```Arguments: extension```", inline=False)
			embed2.add_field(name="reload", value="Reloads the specific extension/category. If the extension is not loaded, it will try to load it.\n```Arguments: extension```", inline=False)
			embed.set_footer(text="Made with ❤️ by qing")

			embed4 = discord.Embed(color=ctx.author.color, title="Commands for category 'DiscordUtils'", description="This category is for commands that checks specific information from Discord.")
			embed4.add_field(name="changeprefix", value="[Administrator only] Change the bot prefix of the current guild.\n```Arguments: prefix```", inline=False)
			embed4.add_field(name="help", value="Shows this message.\n```Arguments: None```", inline=False)
			embed4.add_field(name="userinfo", value="Shows the account information of the user.\n```Arguments: @user```", inline=False)
			embed4.add_field(name="serverinfo", value="Shows the server information of the current guild.\n```Arguments: None```", inline=False)
			embed4.add_field(name="say", value="Returns what the user inputs\n```Arguments: text```", inline=False)
			embed4.add_field(name="ping", value="Display the latency for the bot to receive a response from the user's message.\n```Arguments: None```", inline=False)
			embed4.add_field(name="prefix", value="Returns the prefix for the current guild.\n```Arguments: None```", inline=False)
			embed4.add_field(name="invite", value="Returns the invite link of the bot.\n```Arguments: None```", inline=False)
			embed4.add_field(name="bug", value="Run this if you found a bug while using the bot.\n```Arguments: None```", inline=False)
			embed4.add_field(name="avatar", value="Returns the avatar of the user.\n```Arguments: @user```", inline=False)
			embed4.add_field(name="api", value="Returns a list of APIs that are used for the bot.\n```Arguments: None```", inline=False)
			embed4.add_field(name="repository", value="Returns the github link for the bot.\n```Arguments: None```", inline=False)
			embed4.add_field(name="help_old", value="Shows the old help command that is planned to be deprecated on 1/1/2022 (<t:1672531200:R>)\n```Arguments: page number```", inline=False)
			embed4.set_footer(text="Made with ❤️ by qing")

			embed5 = discord.Embed(color=ctx.author.color, title="Commands for category 'Fun (1)'", description="This category is for commands that usually is fun and trolling.")
			embed5.add_field(name="uncover", value="Ooo! This person was hiding behind the wall all the time?!\n```Arguments: @user```", inline=False)
			embed5.add_field(name="drip", value="Pretend you're a rich person by wearing a fake expensive jacket!\n```Arguments: @user```", inline=False)
			embed5.add_field(name="alert", value="Make a fake iPhone alert picture!\n```Arguments: text```", inline=False)
			embed5.add_field(name="ship", value="Make a lovely combination of 2 people's avatars!\n```Arguments: @user1 @user2```", inline=False)
			embed5.add_field(name="biden", value="Make Biden tweet anything!\n```Arguments: text```", inline=False)
			embed5.add_field(name="wouldyourather", value="Get Would You Rather Questions!\n```Arguments: None```", inline=False)
			embed5.add_field(name="8ball", value="Ask the 8ball some questions.\n```Arguments: question```", inline=False)
			embed5.add_field(name="unforgivable", value="Did you know that some sins are unforgivable?\n```Arguments: text```", inline=False)
			embed5.add_field(name="showerthoughts", value="Get random Shower Thoughts!\n```Arguments: None```", inline=False)
			embed5.add_field(name="pickuplines", value="Get some pickup lines to use.\n```Arguments: None```", inline=False)
			embed5.add_field(name="texttomorse", value="Convert text to morse code!\n```Arguments: text```", inline=False)
			embed5.add_field(name="oogway", value="Create an 'Oogway Quote' meme!\n```Arguments: text```", inline=False)
			embed5.add_field(name="caution", value="A caution banner that looks real!\n```Arguments: text```", inline=False)
			embed5.add_field(name="decodebinary", value="Decode binary numbers into text!\n```Arguments: integers```", inline=False)
			embed5.add_field(name="encodebinary", value="Encode text into binary numbers!\n```Arguments: text```", inline=False)
			embed5.add_field(name="quote", value="Get random Quotes!\n```Arguments: None```", inline=False)
			embed5.add_field(name="wanted", value="Create a fake wanted poster with your image!\n```Arguments: @user```", inline=False)
			embed5.add_field(name="carpic", value="Returns random car pictures.\n```Arguments: None```", inline=False)
			embed5.add_field(name="jail", value="Jail overlay on image.\n```Arguments: @user```", inline=False)
			embed5.add_field(name="sadcat", value="Make a Sad Cat Meme!\n```Arguments: text```", inline=False)
			embed5.add_field(name="chat", value="Chat with the chatbot.\n```Arguments: text```", inline=False)
			embed5.add_field(name="whowouldwin", value="Make a WhoWouldWin meme!\n```Arguments: @user1 @user2```", inline=False)
			embed5.add_field(name="gun", value="Get a perfect Gun overlay on your image!\n```Arguments: @user```", inline=False)
			embed5.add_field(name="reverse", value="Returns your text, but reversed.\n```Arguments: text```", inline=False)
			embed5.add_field(name="ad", value="Make yourself an ad!\n```Arguments: @user```", inline=False)
			embed5.set_footer(text="Made with ❤️ by qing")        

			embed6 = discord.Embed(color=ctx.author.color, title="Commands for category 'Fun (2)'", description="This category is for commands that usually is fun and trolling.")
			embed6.add_field(name="blur", value="Blur an image.\n```Arguments: @user```", inline=False)
			embed6.add_field(name="doublestruck ", value="Convert your text into the doublestruckfont!\n```Arguments: @user```", inline=False)
			embed6.add_field(name="pat", value="Pat an image.\n```Arguments: @user```", inline=False)
			embed6.add_field(name="pikachu", value="Surprised pikachu! :0\n```Arguments: text```", inline=False)
			embed6.add_field(name="invert", value="Invert the colors of an image!\n```Arguments: @user```", inline=False)
			embed6.add_field(name="greyscale", value="Returns the greyscaled version of an image!\n```Arguments: @user```", inline=False)
			embed6.add_field(name="nitro", value="Generate a nitro link!\n```Arguments: None```", inline=False)
			embed6.set_footer(text="Made with ❤️ by qing")

			embed7 = discord.Embed(color=ctx.author.color, title="Commands for category 'Information'", description="This category is for commands that fetches specific information from APIs and returns it.")
			embed7.add_field(name="osuprofile", value="Account information for the game osu!\n```Arguments: name```", inline=False)
			embed7.add_field(name="github", value="Account information for the website Github.\n```Arguments: name```", inline=False)
			embed7.add_field(name="wangzherongyao", value="Hero information for the game Honor of Kings (王者荣耀).\n```Arguments: name```", inline=False)
			embed7.add_field(name="minecraft", value="Account information for the game Minecraft.\n```Arguments: name```", inline=False)
			embed7.add_field(name="mcskinrendered", value="Rendered skin for the game Minecraft.\n```Arguments: name```", inline=False)
			embed7.add_field(name="mcskinraw", value="Raw skin for the game Minecraft.\n```Arguments: name```", inline=False)
			embed7.add_field(name="whenisthenextmcufilm", value="Returns informations about the next MCU film.\n```Arguments: None```", inline=False)
			embed7.add_field(name="shorten", value="Shorten a link!\n```Arguments: url```", inline=False)
			embed7.add_field(name="expand", value="Expand a shortened link!\n```Arguments: url```", inline=False)
			embed7.add_field(name="anime", value="Returns random anime images. `.anime list` for more.\n```Arguments: category```", inline=False)
			embed7.add_field(name="pi", value="22÷7\n```Arguments: None```", inline=False)
			embed7.add_field(name="imdb", value="Returns the information about a movie.\n```Arguments: name```", inline=False)
			embed7.add_field(name="periodictable", value="Retuns the information about specific element in the periodic table.\n```Arguments: element```", inline=False)
			embed7.add_field(name="colour", value="Returns the information about specific colour. `.colour random` for a random colour.\n```Arguments: colour(color)```", inline=False)
			embed7.add_field(name="subreddit", value="Returns the information about specific subreddit.\n```Arguments: name```", inline=False)
			embed7.add_field(name="paper", value="Returns the download link for the specific version of PaperMC.\n```Arguments: version```", inline=False)
			embed7.add_field(name="valorant", value="Returns the information about specific agent/player for the game VALORANT. `.valorant help` for more.\n```Arguments: commandname, name(#tag)```", inline=False)
			embed7.add_field(name="fifaworldcup", value="Returns the information about the 2022 FIFA World Cup.\n```Arguments: country```", inline=False)
			embed7.set_footer(text="Made with ❤️ by qing")

			embed10 = discord.Embed(color=ctx.author.color, description="Now your familiar with the commands, react to ⏪ to go back to the first page if you want to.")
			embed10.add_field(name="To stop this interaction...", value="React to 🚫")
			embed10.set_footer(text="Made with ❤️ by qing")

			self.bot.help_pages = [embed, embed2, embed4, embed5, embed6, embed7, embed10]

			msg = await ctx.reply(embed=self.bot.help_pages[current])
			
			for x in reactions:
				await msg.add_reaction(x)

			while True:
				try:
					def check(reaction, user):
						return user == ctx.author and ctx.message.channel == reaction.message.channel

					reaction = await self.bot.wait_for("reaction_add", check=check, timeout=30.0)

				except asyncio.TimeoutError:
					return

				else:
					previous_page = current
					if "⏪" == reaction[0].emoji:
						current = 0
						for y in reaction:
							await msg.remove_reaction("⏪", ctx.author)
					elif "⬅️" == reaction[0].emoji:
						if current > 0:
							current -= 1
						for y in reaction:
							await msg.remove_reaction("⬅️", ctx.author)
					elif "➡️" == reaction[0].emoji:
						if current < len(self.bot.help_pages)-1:
							current += 1
						for y in reaction:
							await msg.remove_reaction("➡️", ctx.author)
					elif "⏩" == reaction[0].emoji:
						current = len(self.bot.help_pages) - 1
						for y in reaction:
							await msg.remove_reaction("⏩", ctx.author)
					elif "🚫" == reaction[0].emoji:
						await msg.edit(embed=discord.Embed(description="Process terminated"), content="", delete_after=15)
						for y in reaction:
							await msg.remove_reaction("🚫", ctx.author)
						return

					if current != previous_page:
						await msg.edit(embed=self.bot.help_pages[current])

async def setup(bot):
	await bot.add_cog(DiscordUtils(bot))