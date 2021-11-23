from discord.ext import commands

OVERRIDE_CHANNEL = 814213585939988527

class IncorrectGuild(commands.CommandError):
	pass

def check_enabled_guild(ctx, guild_id:int, error:bool=False):
		if ctx.guild is None:
			raise commands.NoPrivateMessage
		if ctx.guild.id == guild_id or ctx.channel.id == OVERRIDE_CHANNEL:
			return True
		else:
			if error:
				raise IncorrectGuild
			else:
				return False

def limit_to_guild(guild:int):
	def predicate(ctx):
		try:
			guild_id = ctx.guild.id
			channel_id = ctx.channel.id
		except AttributeError as err:
			raise commands.NoPrivateMessage from err
		if guild_id == guild or channel_id == OVERRIDE_CHANNEL:
			return True
		else:
			raise IncorrectGuild
			# a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
	return commands.check(predicate)

def limit_to_guilds(*guilds:int):
	def predicate(ctx):
		output = 0
		try:
			guild_id = ctx.guild.id
			channel_id = ctx.channel.id
		except AttributeError as err:
			raise commands.NoPrivateMessage from err
		for guild in guilds:
			if guild_id == guild:
				output += 1
		if output == 1 or channel_id == 814213585939988527:
			return True
		else:
			raise IncorrectGuild
			# a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
	return commands.check(predicate)
	