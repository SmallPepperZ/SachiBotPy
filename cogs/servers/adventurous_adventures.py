import os
import datetime

import discord
from discord.ext import commands
from customfunctions import config,DBManager, CustomChecks
from customfunctions import master_logger,del_msg

# region Variable Stuff

logger = master_logger.getChild("adventureous_adventures")
embedcolor = config("embedcolor")
database = DBManager.Database()

# endregion



class AACog(commands.Cog, name="Server/Adventurous Adventures"):
	def __init__(self, bot):
		self.bot:discord.Client = bot
		self.guild_limit = 855519898025459782
	
	async def cog_check(self, ctx):
		enabled = CustomChecks.check_enabled_guild(ctx, self.guild_limit, True)
		return enabled

	@commands.group(aliases=["aa"])
	async def adventureousadventures(self, ctx):
		"""Commands for the Adventureous Adventures server
		"""
		if ctx.invoked_subcommand is None:
			await ctx.reply("Run `%help adventureousadventures` for subcommands")
	
	@adventureousadventures.command()
	async def start(self, ctx):
		if not ctx.author.id in (545463550802395146,749415687897743371):
			await ctx.send("You cannot run this command")
			return
		else:
			await ctx.message.add_reaction('<a:loading:846527533691568128>')
			cmd = os.popen('"$HOME/Minecraft Servers/Adventureous Adventures/S3/script-run.sh"')
			await ctx.message.remove_reaction('<a:loading:846527533691568128>', ctx.guild.me)
			await ctx.reply(cmd.read().replace(os.getenv("USER"), ""))

	@adventureousadventures.command()
	async def stop(self, ctx):
		if not ctx.author.id in (545463550802395146,749415687897743371):
			await ctx.send("You cannot run this command")
			return
		else:
			await ctx.message.add_reaction('<a:loading:846527533691568128>')
			cmd = os.popen('"$HOME/Minecraft Servers/Adventureous Adventures/S3/script-stop.sh"')
			await ctx.message.remove_reaction('<a:loading:846527533691568128>', ctx.guild.me)
			await ctx.reply(cmd.read().replace(os.getenv("USER"), ""))

def setup(bot):
	bot.add_cog(AACog(bot))
