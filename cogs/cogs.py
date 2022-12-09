from discord.ext import commands
extensions = ["fun", "discordutils", "information", "cogs"]
extensionlist = ["`fun`", "`discordutils`", "`information`", "`cogs`"]
extensions2 = ["fun", "discordutils", "information"]
not_allowed_extensions = ["cogs"]

class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("'Cog' is loaded!")

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension = None):
        if extension is None:
            await ctx.reply("Please specify an extension to load!")
        else:
            if extension not in extensions:
                if str(extension).lower() != "all":
                    await ctx.reply("That extension does not exist!")
                else:
                    msg = await ctx.reply("Loading all extensions...")
                    for x in extensions2:
                        try:
                            await self.bot.load_extension(f"cogs.{x}")
                            await msg.edit(content = f"Loaded {x}")
                        except Exception as e:
                            await ctx.reply(content = f"An error occurred while loading all extensions:\n{e}")
                    await msg.edit(content = "All extensions loaded!")
            else:
                msg = await ctx.reply(f"Loading extension {extension}...")
                try:
                    await self.bot.load_extension(f'cogs.{extension}')
                    await msg.edit(content = f"Extension {extension} loaded!")
                except commands.errors.ExtensionAlreadyLoaded as exception:
                    try:
                        await msg.edit(content = f"The extension {extension} already loaded!")
                    except Exception as e:
                        await msg.edit(content = f"An error occured:\n{e}")
                        return
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension = None):
        if extension is None:
            await ctx.reply("Please specify an extension to unload!")
        else:
            if extension not in extensions:
                if str(extension).lower() != "all":
                    await ctx.reply("That extension does not exist!")
                else:
                    msg = await ctx.reply("Unloading all extensions...")
                    for x in extensions2:
                        try:
                            await self.bot.unload_extension(f"cogs.{x}")
                            await msg.edit(content = f"Unloaded {x}")
                        except Exception as e:
                            await ctx.reply(content = f"An error occured while unloading all extensions:\n{e}")
                    await msg.edit(content="All extensions unloaded!")
            else:
                if str(extension).lower() in not_allowed_extensions:
                    await ctx.reply("This extension cannot be unloaded!")
                    return
                else:
                    msg = await ctx.reply(f"Unloading extension {extension}...")
                    try:
                        await self.bot.unload_extension(f'cogs.{extension}')
                        await msg.edit(content = f"Extension {extension} unloaded!")
                    except Exception as e:
                        await msg.edit(content = f"An error occured:\n{e}")
                        return

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension : str = None):
        if extension is None:
            await ctx.reply("Please specify an extension to reload!")
        else:
            if extension not in extensions:
                if extension.lower() != "all":
                    await ctx.reply("That extension does not exist!")
                else:
                    msg = await ctx.reply("Reloading all extensions...")
                    for x in extensions:
                        try:
                            await self.bot.unload_extension(f"cogs.{x}")
                            await self.bot.load_extension(f"cogs.{x}")
                            await msg.edit(content = f"Reloaded {x}")
                        except commands.errors.ExtensionNotLoaded:
                            try:
                                await self.bot.load_extension(f'cogs.{extension}')
                                await ctx.reply(content = f"Extension {extension} was not loaded. So, {extension} was now loaded!")
                            except Exception as e:
                                await msg.edit(content = f"An error occured:\n{e}")
                    await msg.edit(content = "All extensions reloaded!")
            else:
                msg = await ctx.reply(f"Reloading extension {extension}...")
                try:
                    await self.bot.unload_extension(f'cogs.{extension}')
                    await self.bot.load_extension(f'cogs.{extension}')
                    await msg.edit(content = f"Extension {extension} reloaded!")
                except commands.errors.ExtensionNotLoaded:
                    try:
                        await self.bot.load_extension(f'cogs.{extension}')
                        await msg.edit(content = f"Extension {extension} was not loaded. So, {extension} was now loaded!")
                        return
                    except Exception as e:
                        await msg.edit(content = f"An error occured:\n{e}")
                        return
    
    @commands.command(aliases=["coglist"])
    @commands.is_owner()
    async def extensionlist(self, ctx):
        x = "\n".join(extensionlist)
        y = "__List of extensions__:\n"
        await ctx.reply(y + x)

async def setup(bot):
    await bot.add_cog(Cogs(bot))