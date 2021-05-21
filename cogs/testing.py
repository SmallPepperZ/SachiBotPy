import sqlite3
import discord
from discord.ext import commands
from customfunctions import config, CustomUtilities

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
	async def inviteurltester(self, ctx, userid:int):
		user = self.bot.get_user(int(userid))
		try:
			username=user.name
		except AttributeError:
			username="Unknown User"
		channel = ctx.guild.get_channel(797308957478879234)
		invite = await channel.create_invite(reason=f"Invite for {username}", max_uses=1,unique=True, max_age=604800)
		await ctx.send(invite.url)

	@commands.command(enabled=True)
	@commands.is_owner()
	async def errorme(self, ctx):
		raise ValueError



	@commands.command()
	async def testing12(self, ctx):
		owner = await CustomUtilities.get_owner(self.bot)
		await ctx.reply(owner.mention)

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
