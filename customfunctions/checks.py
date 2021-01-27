from discord.ext import commands

class IncorrectGuild(commands.CommandError):
	pass


def limit_to_guild(guild:int):
	def predicate(ctx):
		try:
			guildid = ctx.guild.id
		except AttributeError:
			raise commands.NoPrivateMessage
		if guildid == guild:
			return True
		else:
			raise IncorrectGuild	
			# a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exceptio
	return commands.check(predicate)	

def limit_to_guilds(*guilds:int):
	def predicate(ctx):
		output = 0
		try:
			guildid = ctx.guild.id
		except AttributeError:
			raise commands.NoPrivateMessage
		for guild in guilds:
			if guildid == guild:
				output += 1
		if output == 1:
			return True
		else:
			raise IncorrectGuild
			# a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exceptio
	return commands.check(predicate)	