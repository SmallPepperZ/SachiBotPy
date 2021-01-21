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


class TestingCog(commands.Cog):
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
			print(f'{ctx.message.author.name} ({ctx.message.author.id}) just used \'{prefix}siren\'')







def setup(bot):
    bot.add_cog(TestingCog(bot))