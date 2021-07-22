from customfunctions.funcs.checks import IncorrectGuild
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

	@CustomChecks.limit_to_guild(764981968579461130)
	@commands.command()
	async def server_status(self, ctx):
		"""Gets the status of the Adventureous Adventures server
		"""
		pass

def setup(bot):
	bot.add_cog(AACog(bot))
