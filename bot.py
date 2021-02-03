#region Imports
import requests
import time
import discord
import os, sys, os.path
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import logging
from discord.ext.commands.errors import *
import json
from discord import Status
import traceback
import urllib, urllib.parse
import datetime
import keyring

from customfunctions import CustomChecks
#endregion

#region Variable Stuff

with open('storage/config.json', 'r') as file:
	configjson = json.loads(file.read())

embedcolor = int(configjson["embedcolor"], 16)
token      = keyring.get_password('SachiBotPY', 'discordtoken')

errorlogdir = 'logs/errors/'


prefix           = configjson["prefix"]
start_time_local = time.time()

intents        = discord.Intents.all()
intents.typing = False
bot            = commands.Bot(command_prefix=prefix, intents = intents, case_insensitive=True)

errorchannel = int(configjson["errorchannel"])

bot.start_time = start_time_local
logging.basicConfig(level=logging.DEBUG)
bot.remove_command('help')


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
	if hasattr(ctx.command, 'on_error'):
		#await ctx.message.add_reaction('<:CommandError:804193351758381086>')
		return
	elif isinstance(error, CommandNotFound) or ctx.command.hidden:
		await ctx.message.add_reaction(str('❔'))
		return 
	elif isinstance(error, NotOwner):		
		await ctx.message.add_reaction(str('🔏'))
		return
	elif isinstance(error, DisabledCommand):		
		await ctx.message.add_reaction(str('<:DisabledCommand:804476191268536320>'))
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
		await ctx.message.add_reaction(str('<:Cooldown:804477347780493313>'))
		if str(error.cooldown.type.name) != "default":
			cooldowntype = f'per {error.cooldown.type.name}'
		else:
			cooldowntype = 'global'
		await ctx.reply(f"This command is on a {round(error.cooldown.per, 0)}s {cooldowntype} cooldown. Wait {round(error.retry_after, 1)} seconds", delete_after=min(10, error.retry_after))
		return
	elif isinstance(error, MissingRequiredArgument):
		await ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`", delete_after=30)
		return 
	elif isinstance(error, BadArgument):
		await ctx.reply(f"Invalid argument!\nUsage:`{ctx.command.signature}`", delete_after=30)
		return 
	elif isinstance(error, NoPrivateMessage):
		await ctx.message.add_reaction(str('<:ServerOnlyCommand:803789780793950268>'))
		return
	elif isinstance(error, CustomChecks.IncorrectGuild):
		await ctx.reply(content="This command does not work in this server.", delete_after=10)
		return
	else:
		#Send user a message
		await ctx.message.add_reaction('<:CommandError:804193351758381086>')
		await ctx.reply("Error:\n```"+str(error)+"```\nSmallPepperZ will be informed", delete_after=60)		

		#Get traceback info
		exc = error
		etype = type(exc)
		trace = exc.__traceback__

		lines = traceback.format_exception(etype, exc, trace)
		traceback_text = ''.join(lines)
		
		#Github gist configuration
		with open('storage/config.json', 'r') as file:
			configjson = json.loads(file.read())		
		configjson["errornum"] = int(configjson["errornum"])+1
		traceback_text = traceback_text.replace(configjson["pathtohide"], '')
		apiurl = "https://api.github.com/gists"
		gisttoedit = f'{apiurl}/{configjson["githubgist"]}'
		githubtoken = keyring.get_password('SachiBotPY', 'githubtoken')
		
		headers={'Authorization':'token %s'%githubtoken}
		params={'scope':'gist'}
		content = f'Error - {error} \n\n\n {traceback_text}'
		leadzeroerrornum = f'{configjson["errornum"]:02d}'
		payload={"description":"SachiBot Errors - A gist full of errors for my bot" ,"public":False,"files":{"SachiBotPyError %s.log"%leadzeroerrornum:{"content": content}}}
		#Upload to github gist
		res=requests.patch(gisttoedit,headers=headers,params=params,data=json.dumps(payload))
		j=json.loads(res.text)

		
		#dump configjson to update error numberr
		with open('storage/config.json', 'w') as file:
			json.dump(configjson, file, indent=4)

		#Build and send embed for error channel
		channel = bot.get_channel(errorchannel)
		embed1 = discord.Embed(title=f"Error {leadzeroerrornum}", color=embedcolor)
		embed1.add_field(name="Message Url:", value=ctx.message.jump_url, inline='false')
		embed1.add_field(name="Message:", value=ctx.message.clean_content, inline='true')
		embed1.add_field(name="Author:", value=ctx.message.author.mention, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		#Check if it was in a guild
		try:
			guildname = ctx.guild.name
			channelname = ctx.channel.name
		except:
			guildname = "DM"
			channelname = ctx.author.id
		embed1.add_field(name="Guild:", value=guildname, inline='true')
		embed1.add_field(name="Channel:", value=channelname, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		embed1.add_field(name="Error:", value=f'```{error}```', inline='false')
		embed1.add_field(name="Traceback:", value=f'Traceback Gist - [SachiBotPyError {leadzeroerrornum}.log](https://gist.github.com/SmallPepperZ/{configjson["githubgist"]}#file-sachibotpyerror-{leadzeroerrornum}-log \"Github Gist #{leadzeroerrornum}\") ', inline='false')
		await channel.send(embed=embed1)




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