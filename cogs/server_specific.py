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
	async def roll_members(self, ctx, count:int=1, include:Union[discord.Role, str]=None, exclude:Union[discord.Role, str]=None):
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
		def _get_members(role:Union[discord.Role, str]=None) -> "list[discord.Member]":
			members:"list[discord.Member]" = []
			if role is None:
				return []
			if isinstance(role,discord.Role):
				members = role.members
			else:
				roles = [role.strip() for role in role.strip('][').split(',')]
				for role_id in roles:
					role = ctx.guild.get_role(int(role_id))
					members+=role.members
			return members

		if include is None:
			included = ctx.guild.members
		else:
			included = _get_members(include)

		excluded = _get_members(exclude)
		elegible = [member for member in included if not member in excluded]
		if count > len(elegible):
			await ctx.reply("Not enough members match these criteria")
			return
		chosen = random.sample(elegible, count)
		formatted_chosen = '\n'.join([choice.mention for choice in chosen])
		embed = discord.Embed(title=f"Selected Member{'s' if len(chosen) > 1 else ''}", description=formatted_chosen)
		await ctx.reply(embed=embed)

def setup(bot):
	bot.add_cog(ServerCog(bot))
