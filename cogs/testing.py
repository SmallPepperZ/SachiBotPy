import sqlite3
import discord
from discord.ext import commands
from customfunctions import config

# region Variable Stuff


embedcolor = int(config("embedcolor"), 16)

# endregion

DB_PATH = "storage/SachiBotStorage.db"
dbcon = sqlite3.connect(str(DB_PATH))
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
		embed = discord.Embed(color=embedcolor, description=contents)
		await message.edit(embed=embed)
		await ctx.message.add_reaction('✅')

	@commands.command()
	@commands.is_owner()
	async def errorme(self, ctx):
		await ctx.reply(1/0)

	@commands.command(aliases=['tos'])
	@commands.is_owner()
	async def siren(self, ctx, *content):
		if not content:
			await ctx.reply("Give me something to say!")
		else:
			content = ' '.join(content)
			await ctx.message.delete()
			embed = discord.Embed(title="<a:WeeWooRed:771082566874169394>  " +
								  content+"  <a:WeeWooRed:771082566874169394>", color=0xf21b1b)
			await ctx.send(embed=embed)

	@commands.command()
	async def commandlistold(self, ctx):
		# logging.info(self.get_commands())

		cmd_list = [cmd.name for cmd in self.get_commands()]

		delim = ", "
		command_list = delim.join(list(map(str, cmd_list)))
		await ctx.reply(command_list)

	@commands.group()
	async def newexport(self, ctx):
		if ctx.invoked_subcommand is None:
			delim = ", "
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


