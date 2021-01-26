import discord
from discord.ext import commands
import json
import time, datetime
import os, sys
from discord import Status
#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]
prefix = configjson["prefix"]

statuses={
	0: "Playing",
	1: "Streaming",
	2: "Listening to",
	3: "Watching",
	4: "",
	5: "Competing in"

}

#endregion
async def changestatus(self, ctx, type):
	if ctx.guild.me.activity != None:
		await self.bot.change_presence(activity=discord.Activity(type=ctx.guild.me.activity.type, name=ctx.guild.me.activity.name), status=type)
	else:
		await self.bot.change_presence(status=type)


class OwnerCog(commands.Cog,name="Owner"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def restart(self, ctx):
		await ctx.message.delete()
		current_time = time.time()
		start_time = ctx.bot.start_time
		difference = int(round(current_time - start_time))
		uptime = str(datetime.timedelta(seconds=difference))
		embed = discord.Embed(color=embedcolor, title="Restarting...")
		embed.set_footer(text=f"lasted for {uptime}")
		await ctx.send(embed=embed)
		print('Bot restarted by '+str(ctx.author))
		os.system("pm2 restart SachiBot")
		await self.bot.logout()

	@commands.command()
	@commands.is_owner()
	async def stop(self, ctx):
		await ctx.message.delete()
		embed = discord.Embed(color=embedcolor, title="Stopping...")
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.send(embed=embed)
		print('Bot stopped by '+str(ctx.author))
		os.system("pm2 stop SachiBot")
		await self.bot.logout()

	@commands.command()
	@commands.is_owner()
	async def export(self, ctx, channel):
		embed = discord.Embed(color=embedcolor)
		embed.add_field(name="Channel", value=f'{channel}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)
		print('Exported by '+str(ctx.author))

	@commands.group()
	@commands.is_owner()
	async def status(self,ctx):

		if ctx.invoked_subcommand is None:
			status = ctx.guild.me.raw_status
			if status == "online":
				statusemoji = '🟢 - '
				statuscolor = 0x00FF00
			elif status == "offline" or status == "invisible":
				statusemoji = '⚫ - '
				statuscolor = 0x444444
			elif status == "dnd" or status == "do_not_disturb":
				statusemoji = '🔴 - '
				statuscolor = 0xFF0000
			elif status == "idle":
				statusemoji = '🟡 - '
				statuscolor = 0xFFFF00
			else:
				statusemoji = ''
				statuscolor = embedcolor
			embed = discord.Embed(color=statuscolor, title="Status:", description=f'**Status:** {statusemoji}{status} - {statuses[ctx.guild.me.activity.type.value]} {ctx.guild.me.activity.name}')
			await ctx.reply(embed=embed)
	
	@status.command(aliases=['green', 'good'])
	async def online(self, ctx):
		await changestatus(self, ctx, Status.online)
		await ctx.message.add_reaction(str('🟢'))
	@status.command(aliases=['yellow', 'okay', 'ok', 'decent', 'afk'])
	async def idle(self, ctx):
		await changestatus(self, ctx, Status.idle)
		await ctx.message.add_reaction(str('🟡'))

	@status.command(aliases=['red', 'bad', 'broken', 'error', 'donotdisturb'])
	async def dnd(self, ctx):
		await changestatus(self, ctx, Status.dnd)
		await ctx.message.add_reaction(str('🔴'))

	@status.command(aliases=['grey','gray', 'hide', 'offline', 'invis', 'hidden'])
	async def invisible(self, ctx):
		await changestatus(self, ctx, Status.invisible)
		await ctx.message.add_reaction(str('⚫'))
	
	@status.group()
	async def activity(self, ctx):
		print()

	@activity.command()
	async def playing(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status), status=ctx.guild.me.status)
		await ctx.message.add_reaction(str('✅'))

	@activity.command()
	async def competing(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status), status=ctx.guild.me.status)
		await ctx.message.add_reaction(str('✅'))

	@activity.command()
	async def listening(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status), status=ctx.guild.me.status)
		await ctx.message.add_reaction(str('✅'))

	@activity.command()
	async def watching(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status), status=ctx.guild.me.status)
		await ctx.message.add_reaction(str('✅'))

	@status.command()
	async def subcommands(self, ctx):
		delim="\n\n"
		delim2=", "
		subcommands = [f'**{cmd.name}:** \n{delim2.join(list(map(str, cmd.aliases)))}' for cmd in ctx.command.parent.commands]
		embed = discord.Embed(color=embedcolor, title="Status Subcommands:", description=f'**Status:** {delim.join(list(map(str, subcommands)))}')
		await ctx.reply(embed=embed)
def setup(bot):
    bot.add_cog(OwnerCog(bot))