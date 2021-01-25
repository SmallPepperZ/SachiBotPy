import discord
from discord.ext import commands
import json
import os

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
		#		print(cwd+"/logs/channels/"+ctx.guild.name+".csv not found, creating..." )
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
	async def coglist(self, ctx):
		print(self.bot.cogs)
		cogjson=self.bot.cogs
		print(cogjson.keys())
		cogs=[cog for cog in cogjson.keys()]
		print(cogs)
		delim = ", "
		coglist = delim.join(list(map(str, cogs)))
		await ctx.reply(coglist)


	@commands.command()
	async def commandlist(self, ctx):
		#print(self.get_commands())
		
		commands = [cmd.name for cmd in self.get_commands()]
		
		delim = ", "
		cmdlist = delim.join(list(map(str, commands)))
		await ctx.reply(cmdlist)
		#TODO Get all bot commands for help page


		
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