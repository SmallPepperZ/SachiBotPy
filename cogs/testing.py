import discord
from discord.ext import commands
import json
import os
from discord.ext.commands.core import is_owner
from disputils import BotEmbedPaginator
from customfunctions import EmbedMaker
from customfunctions import config

#region Variable Stuff


embedcolor = int(config("embedcolor"), 16)

#endregion
import sqlite3
db_path = "storage/SachiBotStorage.db"
dbcon = sqlite3.connect(str(db_path))
dbcur = dbcon.cursor()

class TestingCog(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot = bot

	
	@commands.command()
	@commands.cooldown(rate=1, per=300)
	@commands.is_owner()
	async def changeinvitehelp(self, ctx, *, contents):
		channel = self.bot.get_channel(792558439863681046)
		message = await channel.fetch_message(804147923285573633)
		embed=discord.Embed(color=embedcolor, description=contents)
		await message.edit(embed=embed)
		await ctx.message.add_reaction('✅')
		


	@commands.command()
	@commands.is_owner()
	async def errorme(self, ctx):
		await ctx.reply(1/0)

	@commands.command(aliases=['tos'])
	@commands.is_owner()
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
		command_list = delim.join(list(map(str, commands)))
		await ctx.reply(command_list)
		

		
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
	async def guild(self, ctx, guild_id: str):
		await ctx.send(f'Exporting Guild {guild_id}...')





def setup(bot):
    bot.add_cog(TestingCog(bot))


"""
user_id              = user_info[0]
invite_message_id    = user_info[1]
invite_activity_type = user_info[2]
field_status         = user_info[3]
field_status_editor  = user_info[4]
field_username       = user_info[5]
field_level          = user_info[6]
field_messages       = user_info[7]
field_mention        = user_info[8]
field_info           = user_info[9]
field_inviter_id     = user_info[10]
"""