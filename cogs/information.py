import discord
import osutools
import datetime
import skingrabber
import random
import os
import urlexpander
import pyshorteners
import requests
import aniso8601
import json
import asyncio
import asyncpixel

from dotenv import load_dotenv
from skingrabber import skingrabber
from popcat_wrapper import popcat_wrapper as pop
from discord.ext import commands
from datetime import datetime

load_dotenv()
osua = os.getenv('OSUAPI')
osu = osutools.OsuClientV1(osua)
bitlyapikey = os.getenv("BITLYAPI")
hypixelapi = os.getenv("HYPIXELAPI")

class Information(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("'Information' is loaded!")

	@commands.command(aliases=["osu", "oprofile", "osuprof"])
	async def osuprofile(self, ctx, osuname = None):
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

	@commands.command()
	async def github(self, ctx, githubname = None):
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

	@commands.command()
	async def pi(self, ctx):
		await ctx.reply(f"π = 3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912983367336244065664308602139494639522473719070217986094370277053921717629317675238467481846766940513200056812714526356082778577134275778960917363717872146844090122495343014654958537105079227968925892354201995611212902196086403441815981362977477130996051870721134999999837297804995105973173281609631859502445945534690830264252230825334468503526193118817101000313783875288658753320838142061717766914730359825349042875546873115956286388235378759375195778185778053217122680661300192787661119590921642019893809525720106548586327886593615338182796823030195203530185296899577362259941389124972177528347913151557485724245415069595082953311686172785588907509838175463746493931925506040092770167113900984882401285836160356370766010471018194295559619894676783744944825537977472684710404753464620804668425906949129331367702898915210475216205696602405803815019351125338243003558764024749647326391419927260426992279678235478163600934172164121992458631503028618297455570674983850549458858692699569092721079750930295532116534498720275596023648066549911988183479775356636980742654252786255181841757467289097777279380008164706001614524919217321721477235014144197356854816136115735255213347574184946843852332390739414333454776241686251898356948556209921922218427255025425688767179049460165346680498862723279178608578438382796797668145410095388378636095068006422512520511739298489608412848862694560424196528502221066118630674427862203919494504712371378696095636437191728746776465757396241389086583264599581339047802")

	@commands.command()
	async def mcskinrendered(self, ctx, username = None):
		async with ctx.typing():
			sg = skingrabber()
			if username == None:
				await ctx.reply("Your username cannot be blank!")
			else:
				try:
					await ctx.reply(sg.get_skin_rendered(user=username))
				except Exception:
					await ctx.reply("An error occured! Please try checking your input if its a valid Minecraft username.")

	@commands.command()
	async def mcskinraw(self, ctx, username = None):
		async with ctx.typing():
			sg = skingrabber()
			if username == None:
				await ctx.reply("Your username cannot be blank!")
			else:
				try:
					await ctx.reply(sg.get_skin(user=username))
				except Exception:
					await ctx.reply("An error occured! Please try checking your input if its a valid Minecraft username.")

	@commands.command()
	async def whenisthenextmcufilm(self, ctx):
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
			embed.add_field(name="What's behind?", value="Black Panther: Wakanda Forever")
			embed.set_image(url=poster_url)
			await ctx.reply(embed=embed)

	@commands.command(aliases=["shrink"])
	async def shorten(self, ctx, link = None):
		async with ctx.typing():
			if link == None:
				link = "https://qingbotcommand.netlify.app/"
			s = pyshorteners.Shortener(api_key=bitlyapikey)
			output = s.bitly.short(link)
			await ctx.reply(f"Your shorten link is {output} | It has been used for {s.bitly.total_clicks(output)} times")            

	@commands.command()
	async def expand(self, ctx, link = None):
		async with ctx.typing():
			if link == None:
				link = "https://bit.ly/3CrTREY"
			s = urlexpander.expand(link)
			await ctx.reply(f"Your expanded link is {s}")

	@commands.command()
	async def anime(self, ctx, namelist = None):
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

	@commands.command(aliases=["wangzhe", "王者荣耀", "王者", "hok", "honorofkings", "honorofking"])
	async def wangzherongyao(self, ctx, agentname = None):
		async with ctx.typing():
			if agentname == None:
				await ctx.reply("Please input a agent name!")
			else:
				msg = await ctx.reply("Updating JSON file...")
				await asyncio.sleep(1.7)
				await msg.edit(content="Loading JSON file...")
				lol = 'https://pvp.qq.com/web201605/js/herolist.json'
				f = requests.get(lol)
				dt = f.json()
				result = [x for x in dt if x["cname"] == agentname]
				for lsb in result:
					e = lsb["ename"]
					c = lsb["cname"]
					t = lsb["title"]
					n = lsb["new_type"]
					h = lsb["hero_type"]
					sohai = lsb["skin_name"]
					z = lsb["moss_id"]

				with open('wangzhe.json', encoding='utf-8') as sb:
					data = json.load(sb)
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
					embed.add_field(name="Moss ID", value=z)
					embed.add_field(name="Hero code", value=shabi[0:3])
					embed.add_field(name="Hero type", value=h)
					embed.add_field(name="Tips", value=t)
					embed.add_field(name='Skins', value=", ".join(list))
					embed.add_field(name="Url", value=l)
					embed.set_author(name=gannineh, url=l, icon_url=f"https://game.gtimg.cn/images/yxzj/img201606/heroimg/{shabi[0:3]}/{shabi[0:3]}.jpg")
					embed.set_thumbnail(url=f"https://game.gtimg.cn/images/yxzj/img201606/heroimg/{shabi[0:3]}/{shabi[0:3]}-smallskin-2.jpg")
					await msg.edit(content='', embed=embed)

	@commands.command(aliases=["mc"])
	async def minecraft(self, ctx, username=None):
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
				embed.add_field(name="Hypixel build battle score/games played/coins", value=f"{(await hy.player(uuid)).stats.build_battle.score} | {(await hy.player(uuid)).stats.build_battle.games_played} / {(await hy.player(uuid)).stats.build_battle.coins}")
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
			except Exception as e:
				await msg.edit(content=f"Player `{username}` not found")


	@commands.command(aliases=["movie"])
	async def imdb(self, ctx, *, moviename=None):
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

	@commands.command(aliases=["pt", "periodict", "ptable"])
	async def periodictable(self, ctx, *, element = None):
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

	@commands.command(aliases=["colour"])
	async def color(self, ctx, color = None):
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

	@commands.command(aliases=["reddit"])
	async def subreddit(self, ctx, *, subreddit = None):
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

	@commands.command()
	async def paper(self, ctx, version = None):
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

	@commands.command(aliases=["val", "valo"])
	async def valorant(self, ctx, cmdname = None, *, nama = None):
		async with ctx.typing():
			st = ["stats", "account", "stat"]
			ag = ["agent", "hero", "heroes", "agents"]
			hl = ["help", "list"]
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
								embed.add_field(name="Ability 1", value=ming)
								embed.add_field(name="Ability 2", value=min)
								embed.add_field(name="Ability 3 (aka Grenade)", value=mi)
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
			elif cmdname in hl:
				try:
					embed = discord.Embed(color=ctx.author.color, title="Commands list for `.valorant`", description = "`{}` = Required argument | `()` = Optional argument")
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

	@commands.command(aliases=["futsal", "football", "fifaworldcup2022", "fwc2022", "fwc"])
	async def fifaworldcup(self, ctx, *, teamname = None):
		async with ctx.typing():
			email = os.getenv('FIFA2022APIEMAIL')
			password = os.getenv('FIFA2022APIPASSWORD')
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

			if teamname != None:
				try:
					response = requests.get('http://api.cup2022.ir/api/v1/team', headers=headers)
					ts = requests.get('http://api.cup2022.ir/api/v1/standings', headers=headers)
					s = ts.json() 
					r = response.json()

					tmname = teamname[0].upper() + teamname[1:]
					for lsb in r["data"]:
						if lsb["name_en"] == tmname:
							_id = lsb["_id"]
							name_en = lsb["name_en"]
							name_fa = lsb["name_fa"]
							flag = lsb["flag"]
							fifacode = lsb["fifa_code"]
							iso2 = lsb["iso2"]
							group = lsb["groups"]
							id = lsb["id"]

					for sb in s["data"]:
						for h in sb["teams"]:
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

async def setup(bot):
	await bot.add_cog(Information(bot))