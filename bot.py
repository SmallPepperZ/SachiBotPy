import time
import discord
import os
from discord.ext import commands
import logging
import sys
import io

tokentxt = open("token.txt", "r", encoding="utf-8")
token = tokentxt.read()
tokentxt.close()


bot = commands.Bot(command_prefix='%')
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)
bot.remove_command('help')

@bot.event
async def on_ready():
	print('--------------------')
	print('Logged in as')
	print(' - '+bot.user.name)
	print(' - '+str(bot.user.id))
	print('--------------------')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for a %"))
	return

@bot.command()
async def help(ctx):
	await ctx.message.delete()
	embed = discord.Embed(color=0x0c0f27, title="Commands")
	embed.add_field(name="Utilities", value=f'**ping**\nreturns the bot\'s latency \n\n **export**\nexports the specified channel into a csv file on the host machine', inline='true')
	embed.add_field(name="Maintenance", value=f'**stop**\nshuts down the bot\n\n **restart**\nRestarts the bot', inline='true')
	embed.set_footer(text=f"Request by {ctx.author}")
	await ctx.send(embed=embed)
	logging.info('Help triggered by '+str(ctx.author))


@bot.command()
async def ping(ctx):
	await ctx.message.delete()
	embed = discord.Embed(color=0x0c0f27)
	embed.add_field(name="Ping", value=f'🏓 Pong! {round(bot.latency * 1000)}ms')
	embed.set_footer(text=f"Request by {ctx.author}")
#	embed.set_timestamp()
	await ctx.send(embed=embed)
	logging.info('Pinged by '+str(ctx.author))
	

@bot.command()
async def export(ctx, channel):
	embed = discord.Embed(color=0x0c0f27)
	embed.add_field(name="Channel", value=f'{channel}')
	embed.set_footer(text=f"Request by {ctx.author}")
	#embed.add_timestamp()
	await ctx.send(embed=embed)
	print('Exported by '+str(ctx.author))

@bot.command()
@bot.check(commands.is_owner())
async def restart(ctx):
	if commands.NotOwner == True:
		return
	else:
		await ctx.message.delete()
		embed = discord.Embed(color=0x0c0f27, title="Restarting...")
		embed.set_footer(text=f"Request by {ctx.author}")
		await ctx.send(embed=embed)
		logging.warning('Bot restarted by '+str(ctx.author))
		await os.system("python ./bot.py")
		await bot.logout()

@bot.command()
@bot.check(commands.is_owner())
async def stop(ctx):
	if commands.NotOwner == True:
		return
	else:
		await ctx.message.delete()
		embed = discord.Embed(color=0x0c0f27, title="Stopping...")
		embed.set_footer(text=f"Request by {ctx.author}")
		await ctx.send(embed=embed)
		logging.warn('Bot stopped by '+str(ctx.author))
		await bot.stat
		await bot.logout()
		await time.sleep(100)
		await quit()


bot.run('')