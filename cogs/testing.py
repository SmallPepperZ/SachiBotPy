import discord
from discord.ext import commands
import json
import os, logging
from disputils import BotEmbedPaginator
#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)

#endregion


class TestingCog(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.cooldown(rate=1, per=300)
	@commands.check(commands.is_owner())
	async def custom(self, ctx, *, contents):
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
	async def commandlist(self, ctx):
		commandsdict = {}
		for cog in self.bot.cogs.keys():
			commandsdict[str(cog)] = {}
		commands = self.bot.walk_commands()
		
		for cmd in commands:
			if (not cmd.hidden) and cmd.enabled:
				logging.debug("loop started")
				qname =	cmd.qualified_name
				logging.debug('qname')
				description = cmd.description
				logging.debug('description')
				usage = cmd.usage
				logging.debug('usage')
				parent = cmd.full_parent_name
				logging.debug('parent')
				aliases = cmd.aliases
				logging.debug(aliases)
				cog = cmd.cog_name
				logging.debug(cog)
				commandsdict[str(cog)][str(qname)] = {"description": description, "usage": usage, "parent": parent, "aliases": aliases}
				logging.debug("loop finished")
		logging.debug("loop finished (4 real)")
		with open('commands.json', 'w') as file:
			json.dump(commandsdict, file, indent=4)
		logging.debug("dumping to json finished")
		embed = discord.Embed(color=embedcolor, title="Help")
		cogdata = ''
		pages = []
		for cog in commandsdict.keys():
			logging.debug(f"Starting cog loop for {cog}")
			
			#cogdata += str(f'\n\n**{cog}**\n')
			for command in commandsdict[cog].keys():
				logging.debug(f"Starting command loop for {cog}")
				if commandsdict[cog][command]["description"] != '':
					description = f': {commandsdict[cog][command]["description"]}'
				else:
					description = ''
				cogdata += f'\n`{command}`{description}'	
			if not cogdata == '':
				if (cog == "Owner" or cog == "Testing"):
					if ctx.author.id == 545463550802395146:
						pages.append(discord.Embed(title=f'Help: {cog}', description=cogdata, color=embedcolor))	
				elif cog == "MDSP":
					if ctx.guild.id == 764981968579461130:
						pages.append(discord.Embed(title=f'Help: {cog}', description=cogdata, color=embedcolor))
				else:
					pages.append(discord.Embed(title=f'Help: {cog}', description=cogdata, color=embedcolor))
			cogdata = ''
			
		paginator = BotEmbedPaginator(ctx, pages)
		await paginator.run()
		

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