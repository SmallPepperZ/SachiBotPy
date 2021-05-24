import random
from typing import Union
import discord
from discord.ext import commands
from customfunctions import config, CustomChecks

#region Variable Stuff


embedcolor = int(config("embedcolor"), 16)
#endregion


class ServerCog(commands.Cog, name="Server Specific"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@commands.command()
	@CustomChecks.limit_to_guild(846191837684826123)
	async def roll_members(self, ctx, count:int=1, include:Union[discord.Role, "list[discord.Role]"]=None, exclude:Union[discord.Role, "list[discord.Role]"]=None):
		"""Returns random member(s) from a guild

		Parameters
		----------
		count : int
			The number of members to return
		include : Union[discord.Role,list[discord.Role], optional
			Only select members with these roles, by default None
		exclude : Union[discord.Role,list[discord.Role], optional
			Don't select members with these roles, by default None
		"""
		excluded:"list[discord.Member]" = []
		included:"list[discord.Member]" = []
		if isinstance(include,discord.Role):
			included = include.members
		elif isinstance(include,list):
			for role in include:
				included.append(role.members)

		if isinstance(exclude,discord.Role):
			excluded = exclude.members
		elif isinstance(exclude,list):
			for role in exclude:
				excluded.append(role.members)

		if include is None:
			included = ctx.guild.members
		elegible = [member for member in included if not member in excluded]
		try:
			chosen = random.sample(elegible, count)
		except ValueError:
			await ctx.reply("Not enough members match this criteria")
		formatted_chosen = '\n'.join([choice.mention for choice in chosen])
		await ctx.reply(formatted_chosen)

def setup(bot):
	bot.add_cog(ServerCog(bot))
