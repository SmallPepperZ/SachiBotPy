#region Imports
import time
import discord
import os, sys
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import logging
from discord.ext.commands.errors import CommandError
from discord.ext.commands.errors import MissingPermissions, BotMissingPermissions, CommandNotFound
import json
import traceback, linecache
import urllib, urllib.parse
#endregion

#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]


prefix = configjson["prefix"]
start_time_local = time.time()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents = intents)

errorchannel = int(configjson["errorchannel"])

bot.start_time = start_time_local
logging.basicConfig(level=logging.INFO)
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
			   'cogs.logging']

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
	print("Bot initialized")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for a % | %help"))


#region Bot Events

#@bot.event
#async def on_command_error(ctx, error):
#	if isinstance(error, CommandError):
#		try:
#			if isinstance(error, CommandNotFound):
#				await ctx.message.add_reaction(str('❔'))
#				return 
#			if isinstance(error, commands.NotOwner):
#				await ctx.message.add_reaction(str('🔒'))
#			else:
#				try:
#					await ctx.reply("Bot received error :\n```"+str(error)+"```\n Pinging <@545463550802395146>")
#					logging.error("Error: \n"+str(error))
#					return
#				except:
#					return
#		except:
#			return
	
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
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
	elif isinstance(error, CommandError):
		exc = error
		etype = type(exc)
		trace = exc.__traceback__

		lines = traceback.format_exception(etype, exc, trace)
		traceback_text = ''.join(lines)

		channel = bot.get_channel(errorchannel)

		api_dev_key=configjson["pbdevapikey"]
		api_user_key=configjson["pbuserapikey"]
		api_paste_code=urllib.parse.quote_plus(traceback_text)
		api_paste_name=urllib.parse.quote_plus(ctx.message.clean_content)
		api_option="paste"
		api_paste_private="1"
		api_paste_expire_date='1W'
		await ctx.reply("Error:\n```"+str(error)+"```\nSmallPepperZ will be informed")		
		url1 = os.popen(f'curl -s -X POST -d api_option={api_option} -d api_paste_code={api_paste_code} -d api_paste_name={api_paste_name} -d api_dev_key={api_dev_key} -d api_paste_private={api_paste_private} -d api_user_key={api_user_key} -d api_paste_expire_date={api_paste_expire_date} https://pastebin.com/api/api_post.php').read()
		print(url1)
		try:
			url = url1.split("com",1)[0]+'com/raw'+url1.split("com",1)[1]
		except:
			url = url1
		embed1 = discord.Embed(title="Error", color=embedcolor)
		embed1.add_field(name="Message Url:", value=ctx.message.jump_url, inline='false')
		embed1.add_field(name="Message:", value=ctx.message.clean_content, inline='true')
		embed1.add_field(name="Author:", value=ctx.message.author.mention, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		embed1.add_field(name="Guild:", value=ctx.guild.name, inline='true')
		embed1.add_field(name="Channel:", value=ctx.channel.name, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		embed1.add_field(name="Error:", value=f'```{error}```', inline='false')
		embed1.add_field(name="Traceback:", value=url, inline='false')
		await channel.send(embed=embed1)
		
		logging.error("Error: \n"+str(error))
		return



@bot.event
async def on_member_join(member):
	print("someone joined")
	channel = bot.get_channel(797308957478879234)
	await channel.send("hi "+member.name)
#@bot.event
#async def on_message(message):
#	if bot.user.mentioned_in(message):
#		embed = discord.Embed(color=embedcolor)
#		embed.add_field(name="Prefix", value="`%`", inline='true')
#		embed.add_field(name="Help", value="`%help`", inline='true')
#		embed.set_footer(text=f"Request by {message.author}", icon_url= message.author.avatar_url)
#		await message.reply(embed=embed)

#endregion

#region Testing
@bot.command()
@bot.check(commands.is_owner())
async def errorme(ctx):
	await ctx.reply(1/0)


@bot.command()
@bot.check(commands.is_owner())
async def channels(ctx):
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

@bot.command(aliases=['tos'])
@bot.check(commands.is_owner())
async def siren(ctx, *, content:str=None):
	if not content:
		await ctx.reply("Give me something to say!")
	else:
		await ctx.message.delete()
		embed = discord.Embed(title="🚨  "+content+"  🚨", color=0xf21b1b )
		await ctx.send(embed=embed)
		print(f'{ctx.message.author.name} ({ctx.message.author.id}) just used \'{prefix}siren\'')



#endregion

bot.run(token)