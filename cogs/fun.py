import discord
import random
import string
import requests
from popcat_wrapper import popcat_wrapper as pop
from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		print("'Fun' is loaded!")

	@commands.command()
	async def uncover(self, ctx, user : discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			pfp = user.display_avatar.url
			l = f"https://api.popcat.xyz/uncover?image={pfp}"
			res = requests.get(l)
			try:
				with open("alert.png", "wb") as file:
					file.write(res.content)
				await ctx.reply(file = discord.File("alert.png"))
			except Exception:
				await ctx.reply("Something went wrong. Please try again!")

	@commands.command()
	async def drip(self, ctx, user : discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			pfp = user.display_avatar.url
			l = f"https://api.popcat.xyz/drip?image={pfp}"
			res = requests.get(l)
			try:
				with open("drip.png", "wb") as file:
					file.write(res.content)
				await ctx.reply(file = discord.File("drip.png"))
			except Exception:
				await ctx.reply("Something went wrong. Please try again!")

	@commands.command()
	async def alert(self, ctx, * , text = None):
		async with ctx.typing():
			if text == None:
				await ctx.reply("Please input a valid text!")
			else:
				try:
					ft = text.replace(" ", "+")
				except Exception:
					await ctx.reply("An error occured! Please check if it is a valid text!")
					return

				try:
					l = f'https://api.popcat.xyz/alert?text={text}'
					res = requests.get(l)
					open("alert.png", "wb").write(res.content)
					await ctx.reply(file = discord.File("alert.png"))
				except Exception as e:
					embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
					embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
					embed.set_footer(text="Made with ❤️ by qing")
					await ctx.reply(embed=embed)

	@commands.command(aliases=["love"])
	async def ship(self, ctx, user1: discord.User = None, user2: discord.User = None):
		async with ctx.typing():
			if user1 == None:
				await ctx.reply("Please @ a valid discord user (e.g: <@926975122030596196>)")
				return
			elif user2 == None:
				user2 = ctx.author
			try:
				u1 = await self.bot.fetch_user(user1.id)
				u2 = await self.bot.fetch_user(user2.id)

				l = f"https://api.popcat.xyz/ship?user1={u1.avatar.url}&user2={u2.avatar.url}"
				res = requests.get(l)
				open("ship.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("ship.png"))
			except Exception:
				embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
				embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
				embed.set_footer(text="Made with ❤️ by qing")
				await ctx.reply(embed=embed)

	@commands.command()
	async def biden(self, ctx, *, text = f"Made with ❤️ by qing"):
		async with ctx.typing():
			s = text.replace(" ", "+")

			l = f'https://api.popcat.xyz/biden?text={s}'
			res = requests.get(l)
			open("biden.png", "wb").write(res.content)
			await ctx.reply(file = discord.File("biden.png"))

	@commands.command(aliases=["wyr"])
	async def wouldyourather(self, ctx):
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

	@commands.command(aliases = ["8ball"])
	async def _8ball(self, ctx, question = None):
		if question == None:
			await ctx.reply("Please enter a valid question!")
		else:
			r = requests.get("https://api.popcat.xyz/8ball")
			raw = r.json()
			await ctx.reply(raw["answer"])

	@commands.command()
	async def unforgivable(self, ctx, text = None):
		if text == None:
			await ctx.reply("Please enter a valid text!")
		else:
			l = f'https://api.popcat.xyz/unforgivable?text={text}'
			res = requests.get(l)
			open("unforgivable.png", "wb").write(res.content)
			await ctx.reply(file = discord.File("unforgivable.png"))

	@commands.command()
	async def showerthoughts(self, ctx):
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

	@commands.command(aliases=["pickup"])
	async def pickuplines(self, ctx):
		async with ctx.typing():
			l = 'https://api.popcat.xyz/pickuplines'
			r = requests.get(l)
			line = r.json()["pickupline"]
			await ctx.reply(line)

	@commands.command(aliases=["ttm", "textmorse"])
	async def texttomorse(self, ctx, *, text = None):
		async with ctx.typing():
			if text == None:
				await ctx.reply("Please enter a valid text!")
			else:
				ft = text.replace(" ", "%20")
				l = f'https://api.popcat.xyz/texttomorse?text={ft}'
				req = requests.get(l)
				r = req.json()["morse"]
				await ctx.reply(r)

	@commands.command()
	async def oogway(self, ctx, *, text = None):
		async with ctx.typing():
			if text == None:
				await ctx.reply("Please enter a valid text!")
			else:
				ft = text.replace(" ", "+")
				l = f'https://api.popcat.xyz/oogway?text={ft}'
				res = requests.get(l)
				open("oogway.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("oogway.png"))

	@commands.command()
	async def caution(self, ctx, *, text = None):
		async with ctx.typing():
			if text == None:
				await ctx.reply("Please enter a valid text!")
			else:
				ft = text.replace(" ", "+")
				l = f'https://api.popcat.xyz/caution?text={ft}'
				res = requests.get(l)
				open("caution.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("caution.png"))

	@commands.command(aliases=["decodeb", "db", "binarydecode"])
	async def decodebinary(self, ctx, *, text = None):
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

	@commands.command(aliases=["encodeb", "eb", "binaryencode"])
	async def encodebinary(self, ctx, *, text = None):
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

	@commands.command()
	async def quote(self, ctx):
		async with ctx.typing():
			req = requests.get("https://api.popcat.xyz/quote")
			r = req.json()
			q = r["quote"]
			u = r["upvotes"]

			embed = discord.Embed(color=ctx.author.color, title="Random quotes", description=q)
			embed.add_field(name="Upvotes", value=u)
			embed.set_footer(text="Made with ❤️ by qing")
			await ctx.reply(embed=embed)

	@commands.command()
	async def wanted(self, ctx, user: discord.User | str = None):
		async with ctx.typing():
			if isinstance(user, discord.User) or user == None:
				if user == None:
					user = ctx.author
				else:
					user = user
				try:
					pfp = user.display_avatar
					l = f"https://api.popcat.xyz/wanted?image={pfp}"
					res = requests.get(l)
					open("wanted.png", "wb").write(res.content)
					await ctx.reply(file = discord.File("wanted.png"))
				except AttributeError:
					await ctx.reply("User not found!")
			elif isinstance(user, str) and user == "help":
				await ctx.reply("The bot will read the displayed avatar of the user for this server if you mention the user. For his/hers normal avatar, please use his/hers discord account ID instead.")
			else:
				return

	@commands.command(aliases=["car"])
	async def carpic(self, ctx):
		async with ctx.typing():
			l = 'https://api.popcat.xyz/car'
			req = requests.get(l)
			r = req.json()
			img = r["image"]
			t = r["title"]

			res = requests.get(l)
			open("carpic.png", "wb").write(res.content)
			await ctx.reply(file = discord.File("carpic.png"), content = t)

	@commands.command()
	async def jail(self, ctx, user: discord.User | str = None):
		async with ctx.typing():
			if isinstance(user, discord.User) or user == None:
				if user == None:
					user = ctx.author
				else:
					user = user
				try:
					pfp = user.display_avatar
					l = f"https://api.popcat.xyz/jail?image={pfp}"
					res = requests.get(l)
					open("jail.png", "wb").write(res.content)
					await ctx.reply(file = discord.File("jail.png"))
				except AttributeError:
					await ctx.reply("User not found!")
			elif isinstance(user, str) and user == "help":
				await ctx.reply("The bot will read the displayed avatar of the user for this server if you mention the user. For his/hers normal avatar, please use his/hers discord account ID instead.")
			else:
				return

	@commands.command(aliases=["emo"])
	async def sadcat(self, ctx, *, text = None):
		if text == None:
			await ctx.reply("Please enter a valid text!")
		else:
			ft = text.replace(" ", "+")
			l = f"https://api.popcat.xyz/sadcat?text={ft}"
			res = requests.get(l)
			open("emo.png", "wb").write(res.content)
			await ctx.reply(file = discord.File("emo.png"))

	@commands.command()
	async def chat(self, ctx, *, q=None):
		if q == None:
			await ctx.reply("Please enter a valid text!")
		else:
			ft = q.replace(" ", "+")
			l = f'https://api.popcat.xyz/chatbot?msg={ft}&owner=qing&botname=qing+Bot'
			req = requests.get(l)
			r = req.json()["response"]
			await ctx.reply(r)

	@commands.command(aliases=["www"])
	async def whowouldwin(self, ctx, user1: discord.User = None, user2: discord.User = None):
		async with ctx.typing():
			if user1 == None:
				await ctx.reply("Please @ a valid discord user (e.g: <@926975122030596196>")
			elif user2 == None:
				user2 == ctx.author
			try: 
				u1 = await self.bot.fetch_user(user1.id)
				u2 = await self.bot.fetch_user(user2.id)

				l = f"https://api.popcat.xyz/whowouldwin?image1={u1.display_avatar.url}&image2={u2.display_avatar.url}"
				res = requests.get(l)
				open("whowouldwin.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("whowouldwin.png"))
			except Exception:
				embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
				embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
				embed.set_footer(text="Made with ❤️ by qing")
				await ctx.reply(embed=embed)

	@commands.command()
	async def gun(self, ctx, user: discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			else:
				user = user
			
			try:
				l = f"https://api.popcat.xyz/gun?image={user.display_avatar}"
				res = requests.get(l)
				open("gun.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("gun.png"))
			except Exception:
				await ctx.reply("An error occured! Please check if it is a valid user!")

	@commands.command()
	async def reverse(self, ctx, *, text = None):
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

	@commands.command()
	async def ad(self, ctx, user: discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			else:
				user = user

			try:
				l = f'https://api.popcat.xyz/ad?image={user.display_avatar}'
				res = requests.get(l)
				open("ad.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("ad.png"))
			except Exception as e:
				await ctx.reply("An error occured! Please check if it is a valid user!")

	@commands.command()
	async def blur(self, ctx, user: discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			else:
				user = user

			try:
				l = f'https://api.popcat.xyz/blur?image={user.display_avatar}'
				res = requests.get(l)
				open("blur.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("blur.png"))
			except Exception as e:
				await ctx.reply("An error occured! Please check if it is a valid user!")

	@commands.command()
	async def doublestruck(self, ctx, *, text=None):
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
					
	@commands.command()
	async def pat(self, ctx, user : discord.User = None):
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

	@commands.command()
	async def pikachu(self, ctx, *, text = None):
		async with ctx.typing():
			if text == None:
				await ctx.reply("Please input a valid text!")
			else:
				try:
					ft = text.replace(" ", "+")
					l = f"https://api.popcat.xyz/pikachu?text={ft}"
					res = requests.get(l)
					open("pikachu.png", "wb").write(res.content)
					await ctx.reply(file = discord.File("pikachu.png"))
				except Exception as e:
					await ctx.reply("An error occured! Please check your input!")

	@commands.command()
	async def invert(self, ctx, *, user : discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			else:
				user = user
				
			try:
				l = f"https://api.popcat.xyz/invert?image={user.display_avatar}"
				res = requests.get(l)
				open("invert.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("invert.png"))
			except Exception as e:
				await ctx.reply("An error occured! Please check your input!")

	@commands.command(aliases=["grayscale"])
	async def greyscale(self, ctx, user : discord.User = None):
		async with ctx.typing():
			if user == None:
				user = ctx.author
			else:
				user = user

			try:
				l = f"https://api.popcat.xyz/greyscale?image={user.display_avatar}"
				res = requests.get(l)
				open("greyscale.png", "wb").write(res.content)
				await ctx.reply(file = discord.File("greyscale.png"))
			except Exception as e:
				embed = discord.Embed(color=ctx.author.color, title="Uh-oh! An error occured!")
				embed.add_field(name="Try contacting the bot owner.", value=f"[CLICK ME](https://discord.com/users/635765555277725696)")
				embed.set_footer(text="Made with ❤️ by qing")
				await ctx.reply(embed=embed)

	@commands.command()
	async def nitro(self, ctx):
		async with ctx.typing():
			chars = list(string.ascii_lowercase)+list(string.ascii_uppercase)+list(string.digits)
			amt = int(1)
			main = "https://discord.gift/"
			for i in range(amt):
				ending = ""
				for i in range(random.randint(6,16)):
					ending += random.choice(chars)
				await ctx.reply(main+ending)

async def setup(bot):
	await bot.add_cog(Fun(bot))