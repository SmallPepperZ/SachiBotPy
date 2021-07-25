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
		await ctx.reply("Run `%help adventureousadventures` for subcommands")
	
	@commands.command()
	async def start(self, ctx):
		if not ctx.author.id in (545463550802395146,749415687897743371):
			await ctx.send("You cannot run this command")
			return
		else:
			cmd = os.system('"$HOME"/Minecraft Servers/Adventureous Adventures/S3/script-run.sh"')
			if cmd != 0:
				await ctx.reply("something went wrong!")
			else:
				await ctx.reply("Started with no errors, probably?")

def setup(bot):
	bot.add_cog(AACog(bot))
