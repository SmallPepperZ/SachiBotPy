import time, datetime
import discord
from discord import NotFound
import os
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import logging
import random
from datetime import timedelta
from discord.ext.commands.errors import CommandError
from discord.ext.commands import MessageConverter

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
    embed.add_field(name="Fun commands",
                    value=helpfun,
                    inline='true')
    embed.add_field(name="Bot utilities",
                    value=helputility,
                    inline='true')
    embed.add_field(name="Moderation commands",
                    value=helpmod,
                    inline='true')
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
		m11 = str(ctx.author)+" asked me politely to say "+content
		m12 = "I've always wanted to be a simon"
		msg = random.choice([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12])
		await ctx.reply(str(msg))
		logging.warning(content+' echo attempted by '+str(ctx.author))
	else:
		await ctx.message.delete()
		await ctx.send(content)
		logging.warning(content+' echoed by '+str(ctx.author))

@bot.command()
async def delete(ctx, messageid):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('❔'))
		return
	else:
		await ctx.message.delete()
		message = await MessageConverter().convert(ctx, messageid)
		await message.delete()
		logging.warning('delete attempted by '+str(ctx.author))
		
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, CommandError):
		try:
			if isinstance(error, CommandNotFound):
				await ctx.message.add_reaction(str('❔'))
				return 
			else:
				try:
					await ctx.reply("Bot received error :\n```"+str(error)+"```\n Pinging <@545463550802395146>")
					logging.error("Bot Broken: "+str(error))
					return
				except:
					return
		except:
			return


@bot.command()
async def test(ctx):
	await ctx.reply('hi')

bot.run(token)
