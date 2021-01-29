#region Imports
import time
import discord
import os, sys, os.path
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import logging
from discord.ext.commands.errors import CommandError, MissingPermissions, BotMissingPermissions, CommandNotFound, MissingRole, CommandOnCooldown, BadArgument
import json
from discord import Status
import traceback
import urllib, urllib.parse

import customfunctions.checks as customchecks
#endregion

#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]

errorlogdir = 'logs/errors/'


prefix = configjson["prefix"]
start_time_local = time.time()

intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(command_prefix=prefix, intents = intents, case_insensitive=True)

errorchannel = int(configjson["errorchannel"])

bot.start_time = start_time_local
logging.basicConfig(level=logging.DEBUG)
bot.remove_command('help')

with open('help-pages/utility.txt', 'r') as file:
	bot.helputility = file.read()
with open('help-pages/admin.txt', 'r') as file:
	bot.helpadmin = file.read()
with open('help-pages/fun.txt', 'r') as file:
	bot.helpfun = file.read()

#endregion

#region Cogs
bot.coglist = ['cogs.owner',
			   'cogs.fun',
		 	   'cogs.utility',
	 	 	   'cogs.admin',
			   'cogs.cogs',
			   'cogs.logging',
			   'cogs.testing',
			   'cogs.mdsp']

if __name__ == '__main__':
    for extension in bot.coglist:
        bot.load_extension(extension)
#endregion

#region Logger Stuff
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)


#endregion

@bot.event
async def on_ready():
	logging.info("Bot initialized")
	#await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for a % | %help"), status=Status.online)


#region Bot Events
	
@bot.event
async def on_command_error(ctx, error):
	error = getattr(error, "original", error)
	if hasattr(ctx.command, 'on_error'):
		return
	elif isinstance(error, CommandNotFound):
		await ctx.message.add_reaction(str('❔'))
		return 
	elif isinstance(error, commands.NotOwner):
		await ctx.message.add_reaction(str('🔏'))
		return
	elif isinstance(error, MissingPermissions):
		await ctx.message.add_reaction(str('🔐'))
		return
	elif isinstance(error, BotMissingPermissions):
		await ctx.reply("I do not have the requisite permissions")
		return
	elif isinstance(error, MissingRole):
		await ctx.message.add_reaction(str('🔐'))
		return
	elif isinstance(error, CommandOnCooldown):
		await ctx.message.add_reaction(str('🕐'))
		return
	elif isinstance(error, BadArgument):
		await ctx.reply("Invalid argument!")
		return 
	elif isinstance(error, commands.NoPrivateMessage):
		await ctx.message.add_reaction(str('<:ServerOnlyCommand:803789780793950268>'))
		return
	elif isinstance(error, customchecks.IncorrectGuild):
		await ctx.reply(content="This command does not work in this server.", delete_after=10)
	elif isinstance(error, CommandError):
		await ctx.reply("Error:\n```"+str(error)+"```\nSmallPepperZ will be informed")		
		exc = error
		etype = type(exc)
		trace = exc.__traceback__

		lines = traceback.format_exception(etype, exc, trace)
		traceback_text = ''.join(lines)
		
		channel = bot.get_channel(errorchannel)
		
		"""
			api_dev_key=configjson["pbdevapikey"]
			api_user_key=configjson["pbuserapikey"]
			api_paste_code=urllib.parse.quote_plus(traceback_text)
			api_paste_name=urllib.parse.quote_plus(ctx.message.clean_content)
			api_option="paste"
			api_paste_private="1"
			api_paste_expire_date='1W'
			url1 = os.popen(f'curl -s -X POST -d api_option={api_option} -d api_paste_code={api_paste_code} -d api_paste_name={api_paste_name} -d api_dev_key={api_dev_key} -d api_paste_private={api_paste_private} -d api_paste_expire_date={api_paste_expire_date} https://pastebin.com/api/api_post.php').read()
			try:
				url = url1.split("com",1)[0]+'com/raw'+url1.split("com",1)[1]
			except:
				url = url1
		"""	
"""
		errornumber = len([name for name in os.listdir(errorlogdir) if os.path.isfile(os.path.join(errorlogdir, name))])+1
		with open(f'logs/errors/Error {errornumber}.log', 'x') as f:
			f.write(traceback_text)
		embed1 = discord.Embed(title=f"Error {errornumber}", color=embedcolor)
		embed1.add_field(name="Message Url:", value=ctx.message.jump_url, inline='false')
		embed1.add_field(name="Message:", value=ctx.message.clean_content, inline='true')
		embed1.add_field(name="Author:", value=ctx.message.author.mention, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		try:
			guildname = ctx.guild.name
			channelname = ctx.channel.name
		except:
			guildname = "DM"
			channelname = "DM"
		embed1.add_field(name="Guild:", value=guildname, inline='true')
		embed1.add_field(name="Channel:", value=channelname, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		embed1.add_field(name="Error:", value=f'```{error}```', inline='false')
		embed1.add_field(name="Traceback:", value=f'File saved to \'logs/errors/Error {errornumber}.log\'', inline='false')
"""#		await channel.send(embed=embed1)
		#FIXME fix this error handling




@bot.event
async def on_member_join(member:discord.Member):	
	channel = bot.get_channel(member.guild.system_channel)
	await channel.send("Hello, "+member.name)
#@bot.event
#async def on_message(message):
#	if bot.user.mentioned_in(message):
#		embed = discord.Embed(color=embedcolor)
#		embed.add_field(name="Prefix", value="`%`", inline='true')
#		embed.add_field(name="Help", value="`%help`", inline='true')
#		embed.set_footer(text=f"Request by {message.author}", icon_url= message.author.avatar_url)
#		await message.reply(embed=embed)

#endregion


bot.run(token)