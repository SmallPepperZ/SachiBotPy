import discord
from discord.ext import commands
import json
import os, logging

#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]
prefix = configjson["prefix"]
#endregion


class TestingCog(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.check(commands.is_owner())
	async def errorme(self, ctx):
		await ctx.reply(1/0)



	@commands.command()
	@commands.check(commands.is_owner())
	async def channels(self, ctx):
		await ctx.message.delete()
		channels1 = ctx.guild.channels
		cwd = os.popen('pwd').read().rstrip()
		#	try:
		filepath = str(cwd+'/logs/channels/'+ctx.guild.name+'.csv')
		os.remove(filepath)
		#	except:
		#		logging.info(cwd+"/logs/channels/"+ctx.guild.name+".csv not found, creating..." )
		for channel1 in channels1:
			towrite = str(str(channel1.category)+', '+channel1.name+', '+str(channel1.changed_roles))
			with open(str("logs/channels/"+ctx.guild.name+".csv"), 'a') as file_object:
				file_object.write(str(towrite+'\n'))

	@commands.command(aliases=['tos'])
	async def siren(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			await ctx.message.delete()
			embed = discord.Embed(title="<a:WeeWooRed:771082566874169394>  "+content+"  <a:WeeWooRed:771082566874169394>", color=0xf21b1b )
			await ctx.send(embed=embed)

	@commands.command()
	async def commandlist(self, ctx):
		commandsdict = {}
		for cog in self.bot.cogs.keys():
			commandsdict[str(cog)] = {}
		commands = self.bot.walk_commands()
		
		for cmd in commands:
			if (not cmd.hidden) and cmd.enabled:
				logging.info("loop started")
				qname =	cmd.qualified_name
				logging.info(qname)
				description = cmd.description
				logging.info(description)
				usage = cmd.usage
				logging.info(usage)
				parent = cmd.parent.name
				logging.info(parent)
				aliases = cmd.aliases
				logging.info(aliases)
				cog = cmd.cog_name
				logging.info(cog)
				commandsdict[str(cog)][str(qname)] = {"description": description, "usage": usage, "parent": parent, "aliases": aliases}
				logging.info("loop finished")
		logging.info("loop finished") #FIXME WHY WON'T YOU WORK YOU STUPID CODE
		with open('commands.json', 'w') as file:
			json.dump(commandsdict, file, indent=2)
		logging.info("dumping to json finished")
		logging.info(commandsdict)


		"""
		cogdict=self.bot.cogs
		logging.info("got cogs")
		commandlist=[cog.get_commands() for cog in cogdict.values()]
		logging.info("got commands")
		commandnames = [command.name for command in commandlist]
		logging.info("got command names")
		#delim = ", "
		#coglist = delim.join(list(map(str, cogs)))
		await ctx.reply(commandnames)
"""

	@commands.command()
	async def commandlistold(self, ctx):
		#logging.info(self.get_commands())
		
		commands = [cmd.name for cmd in self.get_commands()]
		
		delim = ", "
		cmdlist = delim.join(list(map(str, commands)))
		await ctx.reply(cmdlist)
		

		
	@commands.group()
	async def newexport(self, ctx):
		if ctx.invoked_subcommand is None:
			delim=", "
			subcommands = [cmd.name for cmd in ctx.command.commands]
			await ctx.send(f'Please select one of the subcommands ({delim.join(list(map(str, subcommands)))})')
	
	@newexport.command()
	async def channel(self, ctx, channelid: str):
		await ctx.send(f'Exporting channel {channelid}...')

	@newexport.command()
	async def guild(self, ctx, guildid: str):
		await ctx.send(f'Exporting Guild {guildid}...')

def setup(bot):
    bot.add_cog(TestingCog(bot))