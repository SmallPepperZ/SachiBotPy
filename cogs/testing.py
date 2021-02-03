import discord
from discord.ext import commands
import json
import os, logging
from disputils import BotEmbedPaginator
from customfunctions import EmbedMaker

#region Variable Stuff

with open('storage/config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)

#endregion


class TestingCog(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def testcommand(self, ctx, *, content):
		embed = discord.Embed(title="hi")
		EmbedMaker.AddDescriptionField(embed, "Key", "Value", boldkey=False)
		await ctx.reply(embed=embed)	
	
	@commands.command()
	@commands.cooldown(rate=1, per=300)
	@commands.check(commands.is_owner())
	async def changeinvitehelp(self, ctx, *, contents):
		channel = self.bot.get_channel(792558439863681046)
		message = await channel.fetch_message(804147923285573633)
		embed=discord.Embed(color=embedcolor, description=contents)
		await message.edit(embed=embed)
		


	@commands.command()
	@commands.check(commands.is_owner())
	async def errorme(self, ctx):
		await ctx.reply(1/0)

	@commands.command(aliases=['tos'])
	async def siren(self, ctx, *, content:str=None):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			await ctx.message.delete()
			embed = discord.Embed(title="<a:WeeWooRed:771082566874169394>  "+content+"  <a:WeeWooRed:771082566874169394>", color=0xf21b1b )
			await ctx.send(embed=embed)

		

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