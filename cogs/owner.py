
import time
import datetime
import re

import os
import sys

from io import BytesIO
from PIL import Image

import discord

from discord.ext import commands
from discord.ext.commands.core import is_owner
from discord import Status
from discord.ext.commands.errors import NotOwner


from customfunctions import config, set_config
from customfunctions import ConfirmationCheck
from customfunctions import EmbedMaker
from customfunctions import del_msg
from customfunctions import master_logger

#region Variable Stuff
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

BOT_TALK_CHANNEL = None
BOT_TALK_CHANNEL_OBJ = None
embedcolor       = config("embedcolor")
logger = master_logger.getChild("owner")


statuses={
	0: "Playing",
	1: "Streaming",
	2: "Listening to",
	3: "Watching",
	4: "",
	5: "Competing in"

}

#endregion
def save_status(self):
	set_config('status', (self.bot_member.activity.type, self.bot_member.activity.name, self.bot_member.status))

async def apply_status(self):
	status = config('status')
	await self.bot.change_presence(activity=discord.Activity(type=status[0][1], name=status[1]), status=status[2][1])

async def changestatus(self, ctx, status_type): #pylint:disable=unused-argument
	if self.bot_member.activity is not None:
		await self.bot.change_presence(activity=discord.Activity(type=self.bot_member.activity.type, name=self.bot_member.activity.name), status=status_type)
	else:
		await self.bot.change_presence(status=status_type)
	save_status(self)



class OwnerCog(commands.Cog,name="Owner"):
	def __init__(self, bot):
		self.bot = bot

	@property
	def bot_member(self):
		try:
			return self.bot.guilds[0].me
		except IndexError:
			return None


	@commands.command()
	@commands.is_owner()
	async def restart(self, ctx):
		await del_msg(ctx.message)
		current_time = time.time()
		start_time = ctx.bot.start_time
		difference = int(round(current_time - start_time))
		uptime = str(datetime.timedelta(seconds=difference))
		embed = discord.Embed(color=embedcolor, title="Restarting...")
		embed.set_footer(text=f"lasted for {uptime}")
		await ctx.send(embed=embed)
		os.system("screen -dmS SachiBotRestarter $HOME/.scripts/SachiBotPy/restart.sh")
		#await self.bot.logout()

	@commands.command()
	@commands.is_owner()
	async def stop(self, ctx):
		await del_msg(ctx.message)
		embed = discord.Embed(color=embedcolor, title="Stopping...")
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
		await ctx.send(embed=embed)
		os.system("$HOME/.scripts/SachiBotPy/stop.sh")
		#await self.bot.logout()

	@commands.command()
	@commands.is_owner()
	@commands.guild_only()
	async def export(self, ctx, channel:int):
		embed = discord.Embed(color=embedcolor)
		embed.add_field(name="Channel", value=f'{channel}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
		await ctx.reply(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def embedcolor(self, ctx, color:str):
		colorint      = f"0x{color}"
		oldembedcolor = config("embedcolor")
		try:
			newembedcolor = int(colorint, 16)
		except ValueError:
			await ctx.reply("Invalid Color!")
			return
		embed = discord.Embed(color=embedcolor, title="Embed Color", description = f"Old color: #{oldembedcolor}\nNew color: #{color}")

		#Generate image with specified hex
		hexcolor = f"#{color}"
		image    = Image.new("RGB", (100,100), hexcolor)
		buffer   = BytesIO()
		image.save(buffer, "png")
		buffer.seek(0)
		#Attach image and set thumbnail
		file = discord.File(fp=buffer, filename="colorimage.png")
		embed.set_thumbnail(url='attachment://colorimage.png')

		msg = await ctx.reply(embed=embed, file=file)
		confirmation = await ConfirmationCheck.confirm(self, ctx, msg)
		if confirmation:
			embed = discord.Embed(color=newembedcolor, title="Embed Color Set!", description = f"Old color: #{oldembedcolor}\nNew color: #{color}")
			embed.set_thumbnail(url='attachment://colorimage.png')
			await msg.edit(embed=embed)
			#Update the config file
			set_config("embedcolor", colorint)
			#Reload cogs
			for cog in ctx.bot.coglist:
				self.bot.reload_extension(cog)
		elif confirmation is False:
			embed = discord.Embed(color=embedcolor, title="Embed Color", description = "Embed color unchanged")
			await msg.edit(embed=embed)
		elif confirmation is None:
			await ctx.reply("Confirmation timed out")
			return

	@commands.group()
	@commands.is_owner()
	async def status(self,ctx):


		if ctx.invoked_subcommand is None:
			status = self.bot_member.raw_status
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
			embed = discord.Embed(color=statuscolor, title="Status:", description=f'**Status:** {statusemoji}{status} - {statuses[self.bot_member.activity.type.value]} {self.bot_member.activity.name}')
			await ctx.reply(embed=embed)
			save_status(self)

	@status.command(aliases=['green', 'good'])
	async def online(self, ctx):
		await changestatus(self, ctx, Status.online)
		await ctx.message.add_reaction(str('🟢'))
		save_status(self)

	@status.command(aliases=['yellow', 'okay', 'ok', 'decent', 'afk'])
	async def idle(self, ctx):
		await changestatus(self, ctx, Status.idle)
		await ctx.message.add_reaction(str('🟡'))
		save_status(self)

	@status.command(aliases=['red', 'bad', 'broken', 'error', 'donotdisturb'])
	async def dnd(self, ctx):
		await changestatus(self, ctx, Status.dnd)
		await ctx.message.add_reaction(str('🔴'))
		save_status(self)

	@status.command(aliases=['grey','gray', 'hide', 'offline', 'invis', 'hidden'])
	async def invisible(self, ctx):
		await changestatus(self, ctx, Status.invisible)
		await ctx.message.add_reaction(str('⚫'))
		save_status(self)

	@status.group()
	async def activity(self, ctx): #pylint:disable=unused-argument
		logger.info('activity called')

	@activity.command()
	async def playing(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status), status=self.bot_member.status)
		await ctx.message.add_reaction(str('✅'))
		save_status(self)

	@activity.command()
	async def competing(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=status), status=self.bot_member.status)
		await ctx.message.add_reaction(str('✅'))
		save_status(self)

	@activity.command()
	async def listening(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status), status=self.bot_member.status)
		await ctx.message.add_reaction(str('✅'))
		save_status(self)

	@activity.command()
	async def watching(self, ctx, *, status:str):
		await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status), status=self.bot_member.status)
		await ctx.message.add_reaction(str('✅'))
		save_status(self)

	@status.command()
	async def subcommands(self, ctx):
		delim="\n\n"
		delim2=", "
		subcommands = [f'**{cmd.name}:** \n{delim2.join(list(map(str, cmd.aliases)))}' for cmd in ctx.command.parent.commands]
		embed = discord.Embed(color=embedcolor, title="Status Subcommands:", description=f'**Status:** {delim.join(list(map(str, subcommands)))}')
		await ctx.reply(embed=embed)

	@commands.command()
	@commands.check(is_owner())
	#commands.check(guild_only)
	async def bottalk(self, ctx):
		global BOT_TALK_CHANNEL, BOT_TALK_CHANNEL_OBJ, DM_CHANNEL #pylint:disable=global-variable-undefined
		if BOT_TALK_CHANNEL is None:
			DM_CHANNEL = await self.bot.fetch_user(ctx.author.id)
			await del_msg(ctx.message)
			await DM_CHANNEL.send("Bot talk started, type `stoptalk` to end")
			BOT_TALK_CHANNEL = ctx.channel.id
			BOT_TALK_CHANNEL_OBJ = self.bot.get_channel(BOT_TALK_CHANNEL)
			DM_CHANNEL = await self.bot.fetch_user(ctx.author.id)

	@commands.Cog.listener("on_message")
	async def speak_as_bot(self, msg):
		global BOT_TALK_CHANNEL, BOT_TALK_CHANNEL_OBJ #pylint:disable=global-statement
		if BOT_TALK_CHANNEL is not None:
			if (isinstance(msg.channel, discord.channel.DMChannel)) and (msg.author.id == 545463550802395146):
				if not msg.content == "stoptalk":
					await BOT_TALK_CHANNEL_OBJ.send(msg.content)
				else:
					BOT_TALK_CHANNEL = None
					await msg.reply("Bot talk stopped")
			elif msg.channel.id == BOT_TALK_CHANNEL and not (msg.author.id) == 796509133985153025:
				await DM_CHANNEL.send(f'**{msg.author}:** {msg.content}')

	@commands.command()
	@commands.check(is_owner())
	async def enable_guild(self, ctx, guild_id:int):
		guild_ids = [guild.id for guild in self.bot.guilds]
		if guild_id in guild_ids:
			await ctx.reply(embed=EmbedMaker.simple_embed("I am in that server", embedcolor))

		else:
			await ctx.reply(embed=EmbedMaker.simple_embed("I am not in that server", embedcolor))

	@commands.command()
	@commands.check(is_owner())
	async def exec(self, ctx, *, code:str):
		if int(ctx.author.id) != 545463550802395146:
			raise NotOwner
		code = re.findall('```[\S\s]+```', code) #pylint: disable=anomalous-backslash-in-string
		if len(code) != 0:
			code = code[0]
			code = code.replace('```py', '').replace('```', '').strip()
			code = '\n'.join([f'\t{line}' for line in code.splitlines()])
			function_code = (
			 'async def __exec_code(self, ctx):\n'
			f'{code}')
			await ctx.message.add_reaction('<a:loading:846527533691568128>')
			try:
				exec(function_code) #pylint: disable=exec-used
				output = await locals()['__exec_code'](self, ctx)
				if output:
					formatted_output = '\n'.join(output) if len(code.splitlines()) > 1 else output
					await ctx.reply(embed=EmbedMaker.simple_embed(f"Sucess! Output:\n```\n{formatted_output}\n```", embedcolor))
				await ctx.message.add_reaction('👍')
			except Exception as error: #pylint: disable=broad-except
				await ctx.reply(embed=EmbedMaker.simple_embed(f"Error! Output:\n```{error}```", embedcolor))
				await ctx.message.add_reaction('<:CommandError:804193351758381086>')
			await ctx.message.remove_reaction('<a:loading:846527533691568128>', ctx.guild.me)
		else:
			await ctx.reply("Please put the code in a codeblock")
def setup(bot):
	bot.add_cog(OwnerCog(bot))
