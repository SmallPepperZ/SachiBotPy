
import asyncio
import random
from typing import Union

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


from customfunctions import config, CustomChecks, EmbedMaker
from customfunctions import master_logger
#region Variable Stuff

logger = master_logger.getChild("server_specific")
embedcolor = config("embedcolor")
ALLOWED_ROLES=[855519898025459783,855533279267520522]
#endregion

def _get_members(roles:Union[discord.Role, "list[discord.Role]"]=None) -> "list[discord.Member]": # Get the members from a role or list of roles
	members:"list[discord.Member]" = []
	if roles == [None, None]:
		return []
	if isinstance(roles,discord.Role):
		members = roles.members
	else:
		roles = [role for role in roles if role is not None]
		for role in roles:
			members+=role.members
	return members

def _get_elegible_members(guild:discord.Guild,include:"list[discord.Role]"=None, exclude:"list[discord.Role]"=None) -> "list[discord.Member]": # Get members that have roles in the inclusion list but not in the exclusion list
	if include == [None, None]:
		included = guild.members
	else:
		included = _get_members(include)
	excluded = _get_members(exclude)
	elegible = [member for member in included if not member in excluded]
	return elegible

class ServerCog(commands.Cog, name="Server Specific"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@cog_ext.cog_slash( name="rollmembers",
						description="Returns random members from your current guild",
						guild_ids=[797308956162392094,846191837684826123],
						options=[
							{
								"name": "count",
								"description": "The number of members to return, by default, 1",
								"type":4,
								"required": False
							},
							{
								"name": "elegible-role-1",
								"description": "A member must have this role to be selected",
								"type":8,
								"required": False
							},
							{
								"name": "elegible-role-2",
								"description": "A member must have this role to be selected",
								"type":8,
								"required": False
							},
							{
								"name": "inelegible-role-1",
								"description": "No member with this role will be selected",
								"type":8,
								"required": False
							},
							{
								"name": "inelegible-role-2",
								"description": "No member with this role will be selected",
								"type":8,
								"required": False
							},
							{
								"name": "previously-selected-role-1",
								"description": "any member with this role will be added to the output",
								"type":8,
								"required": False
							}
						],
						permissions={
							846191837684826123: [
								{
									"id":545463550802395146,
									"type":2,
									"permission": True
								},
								{
									"id":545457174567190529,
									"type":2,
									"permission": True
								}
							]
						},
						connector={
										"count": "count",
										"elegible-role-1": "include1",
										"elegible-role-2": "include2",
										"inelegible-role-1": "exclude1",
										"inelegible-role-2": "exclude2",
										"previously-selected-role-1":"existing"
									}
									)
	async def _roll_members(self, ctx:SlashContext, count:int=1, include1:discord.Role=None,include2:discord.Role=None, exclude1:discord.Role=None, exclude2:discord.Role=None, existing:discord.Role=None):
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
		include = [include1, include2]
		exclude = [exclude1, exclude2]
		elegible = _get_elegible_members(ctx.guild, include, exclude)
		if len(elegible) < count:
			await ctx.send(hidden=True,content=f"Not enough elegible members, {len(elegible)} elegible members found, {count} requested")
			return
		chosen = random.sample(elegible, count)
		if existing is not None:
			chosen=existing.members+chosen
		formatted_chosen = '\n'.join([f'{chosen.index(choice)+1} - {choice.mention}' for choice in chosen])
		embed = discord.Embed(title=f"Selected Member{'s' if len(chosen) > 1 else ''}", description=formatted_chosen,color=embedcolor)
		await ctx.send(embed=embed)



	@commands.command()
	@CustomChecks.limit_to_guild(846191837684826123)
	async def roll_members_is_rigged(self, ctx):
		customer_satisfaction_message:discord.Message = await ctx.reply(embed=EmbedMaker.simple_embed("I'm sorry you feel that way, please fill out our [customer satisfaction form](https://tinyurl.com/sachibotcustomersupport) so we can improve next time",embedcolor))
		await asyncio.sleep(20)
		await customer_satisfaction_message.delete()
		await ctx.reply(embed=discord.Embed(title="It isn't rigged™", description="This bot is open source on [this github repository](https://github.com/SmallPepperZ/SachiBotPy/blob/development/cogs/server_specific.py#L127). I've highlighted the line where the randomness takes place to enhance your viewing experience. I encourage you to let me know of any issues you find in the code",color=embedcolor))
	
	@cog_ext.cog_slash( name="addrole",
						description="Gives yourself a role",
						guild_ids=[797308956162392094,855519898025459782],
						options=[
							{
								"name": "role",
								"description": "The role to add to yourself. Only works with",
								"type":8,
								"required": True
							}
						],
						connector={"role": "role"}
									)
	async def _add_role(self, ctx:SlashContext, role:discord.Role):
		
		if role in ctx.author.roles:
			await ctx.send(f"You already have {role.mention}",hidden=True)
			logger.debug(f"{ctx.author} tried to add {role.name}, but already had it")
		elif role.id in ALLOWED_ROLES:
			await ctx.author.add_roles(role,reason="Self-added role")
			await ctx.send(f"{role.mention} added successfully",hidden=True)
			logger.debug(f"{ctx.author} added {role.name}")
		else:
			role_mentions=[(ctx.guild.get_role(role)).mention for role in ALLOWED_ROLES]
			await ctx.send(f"You can only add the following roles:\n{', '.join(role_mentions)}",hidden=True)
			logger.debug(f"{ctx.author} tried to add {role.name}, but it wasn't available")


	@cog_ext.cog_slash( name="removerole",
						description="Removes a role from yourself",
						guild_ids=[797308956162392094,855519898025459782],
						options=[
							{
								"name": "role",
								"description": "The role to remove from yourself. Only works with",
								"type":8,
								"required": True
							}
						],
						connector={"role": "role"}
									)
	async def _rem_role(self, ctx:SlashContext, role:discord.Role):
		if role not in ctx.author.roles:
			await ctx.send(f"You don't have {role.mention}",hidden=True)
			logger.debug(f"{ctx.author} tried to remove {role.name}, but didn't have it")
		elif role.id in ALLOWED_ROLES:
			await ctx.author.remove_roles(role,reason="Self-removed role")
			await ctx.send(f"{role.mention} removed successfully",hidden=True)
			logger.info(f"{ctx.author} removed {role.name}")
		else:
			role_mentions=[(ctx.guild.get_role(role)).mention for role in ALLOWED_ROLES]
			await ctx.send(f"You can only add or remove the following roles:\n{', '.join(role_mentions)}",hidden=True)
			logger.debug(f"{ctx.author} tried to remove {role.name}, but it wasn't available")

def setup(bot):
	bot.add_cog(ServerCog(bot))
