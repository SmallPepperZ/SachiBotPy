import time, datetime
import discord
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import logging
import random
from datetime import timedelta

#from datetime import datetime

tokentxt = open("token.txt", "r", encoding="utf-8")
token = tokentxt.read()
tokentxt.close()

color = 0x045e01
prefix = '%'
start_time = time.time()

bot = commands.Bot(command_prefix=prefix)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)
bot.remove_command('help')

@bot.event
async def on_ready():
	print("Bot initialized")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for a %"))
	return

@bot.command()
async def help(ctx):
	await ctx.message.delete()
	embed = discord.Embed(color=color, title="Commands")
	embed.add_field(name="Utilities", value=f'**ping**\nreturns the bot\'s latency \n\n **export**\nexports the specified channel into a csv file on the host machine', inline='true')
	embed.add_field(name="Maintenance", value=f'**stop**\nshuts down the bot\n\n **restart**\nRestarts the bot', inline='true')
	embed.set_footer(text=f"Request by {ctx.author}")
	await ctx.send(embed=embed)
	logging.info('Help triggered by '+str(ctx.author))


@bot.command()
async def ping(ctx):
	await ctx.message.delete()
	current_time = time.time()
	difference = int(round(current_time - start_time))
	uptime = str(datetime.timedelta(seconds=difference))
	embed = discord.Embed(color=color)
	embed.add_field(name="Ping", value=f'🏓 Pong! {round(bot.latency * 1000)}ms', inline='false')
	embed.add_field(name="Uptime", value=f'{uptime}')
	embed.set_footer(text=f"Request by {ctx.author}")
#	embed.set_timestamp()
	await ctx.send(embed=embed)
	logging.warning('Pinged by '+str(ctx.author))
	

@bot.command()
async def export(ctx, channel):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('🔒'))
		return
	else:
		await ctx.message.delete()
		embed = discord.Embed(color=color)
		embed.add_field(name="Channel", value=f'{channel}')
		embed.set_footer(text=f"Request by {ctx.author}")
		#embed.add_timestamp()
		await ctx.send(embed=embed)
		logging.warning('Exported by '+str(ctx.author))

@bot.command()
#@bot.check(commands.is_owner())
async def restart(ctx):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('🔒'))
		return
	else:
		await ctx.message.delete()
		current_time = time.time()
		difference = int(round(current_time - start_time))
		uptime = str(datetime.timedelta(seconds=difference))
		embed = discord.Embed(color=color, title="Restarting...")
		embed.set_footer(text=f"lasted for {uptime}")
		await ctx.send(embed=embed)
		logging.warning('Bot restarted by '+str(ctx.author))
		await os.system("pm2 restart 0")
		await bot.logout()

@bot.command()
#@bot.check(commands.is_owner())
async def stop(ctx):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('🔒'))
		return
	else:
		await ctx.message.delete()
		embed = discord.Embed(color=color, title="Stopping...")
		embed.set_footer(text=f"Request by {ctx.author}")
		await ctx.send(embed=embed)
		logging.warning('Bot stopped by '+str(ctx.author))
		await os.system("pm2 stop 0")
		await bot.logout()

@bot.command()
#@bot.check(commands.is_owner())
async def repeatembed(ctx, *, content:str):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('🔒'))
		return
	else:
		await ctx.message.delete()
		embed = discord.Embed(color=color, description=content)
		await ctx.send(embed=embed)
		logging.warning(content+' echoed by '+str(ctx.author))

@bot.command()
#@bot.check(commands.is_owner())
async def simonsays(ctx, *, content:str):
	if ctx.message.author.id != 545463550802395146: 
		m1 = ":| You can't push me around like that"
		m2 = "You literally typed 11 extra characters to try and get me to do something for you"
		m3 = "Um, no thanks"
		m4 = "I'd reallly rather not say that"
		m5 = "Just say it yourself"
		m6 = "C'mon, just... just remove '%simonsays' and it works"
		m7 = "I am not your speech bot"
		m8 = "You aren't paying me, so no thanks"
		m9 = "I don't work for free"
		m10 = "Make your own simonsays bot"
		msg = random.choice([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10])
		await ctx.reply(str(msg))
		logging.warning(content+' echo attempted by '+str(ctx.author))
	else:
		await ctx.message.delete()
		await ctx.send(content)
		logging.warning(content+' echoed by '+str(ctx.author))

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandNotFound):
		await ctx.message.add_reaction(str('❔'))
		return 

@bot.command()
async def test(ctx):
	await ctx.reply('hi')

bot.run(token)