#region Imports
import time
import discord
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import logging
import random
from discord.ext.commands.errors import CommandError
import json

#endregion

#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]


prefix = configjson["prefix"]
start_time_local = time.time()

bot = commands.Bot(command_prefix=prefix)
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
	 	 	   'cogs.admin']

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

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandError):
		try:
			if isinstance(error, CommandNotFound):
				await ctx.message.add_reaction(str('❔'))
				return 
			if isinstance(error, commands.NotOwner):
				await ctx.message.add_reaction(str('🔒'))
			else:
				try:
					await ctx.reply("Bot received error :\n```"+str(error)+"```\n Pinging <@545463550802395146>")
					logging.error("Bot Broken: \n"+str(error))
					return
				except:
					return
		except:
			return


@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if (message.guild.id == 764981968579461130) and (message.channel.id != 789195444957609994) and (message.channel.id != 789607866780745748):
		sentmsg2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+", "+str(message.channel.id)+", "+str(message.channel.name)+", "+str(message.author)+", "+str(message.content)
		print(sentmsg2)
		with open("logs/test.csv", 'a') as file_object:
			file_object.write(sentmsg2+"\n")

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
		print(content+' echoed by '+str(ctx.author))



#endregion

bot.run(token)