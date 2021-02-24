from discord.ext import commands

class IncorrectGuild(commands.CommandError):
	pass


def limit_to_guild(guild:int):
	def predicate(ctx):
		try:
			guild_id = ctx.guild.id
			channel_id = ctx.channel.id
		except AttributeError:
			raise commands.NoPrivateMessage
		if guild_id == guild or channel_id == 814213585939988527:
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
		except AttributeError:
			raise commands.NoPrivateMessage
		for guild in guilds:
			if guild_id == guild:
				output += 1
		if output == 1 or channel_id == 814213585939988527:
			return True
		else:
			raise IncorrectGuild
			# a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
	return commands.check(predicate)	