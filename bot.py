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

with open('help-pages/utility.txt', 'r') as file:
	helputility = file.read()
with open('help-pages/admin.txt', 'r') as file:
	helpadmin = file.read()
with open('help-pages/fun.txt', 'r') as file:
	helpfun = file.read()

embedcolor = 0x045e01
prefix = '%'
start_time = time.time()

bot = commands.Bot(command_prefix=prefix)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO) # Do not allow DEBUG messages through
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("{asctime}: {levelname}: {name}: {message}", style="{"))
logger.addHandler(handler)
bot.remove_command('help')

@bot.event
async def on_ready():
	print("Bot initialized")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for a %"))
	while True: #loop (running your bot non-stop, so you just have to write "flip" in terminal to run it)
		command = str(input())
		if command.startswith("discord-say") == True:
			print("Test")
		#	channel1 = client.get_channel(1234567890) 
		#	await channel1.send("It's {}!" .format(a)

@bot.command(aliases=['commands'])
async def help(ctx):
	embed = discord.Embed(color=embedcolor, title="Commands")
	embed.add_field(name="__Utilities__", value=helputility, inline='true')
	embed.add_field(name="__Fun__", value=helpfun, inline='true')
	embed.add_field(name="__Owner__", value=helpadmin, inline='false')
	
	embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
	await ctx.reply(embed=embed)
	print('Help triggered by '+str(ctx.author))

@bot.command()
async def purge(ctx):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('🔒'))
		return
	else:
		args = ctx.message.content.split(" ")
		if args[1]:
			try:
				amount = int(args[1])
				await ctx.message.delete()				
				await ctx.channel.purge(limit=amount)
				embed = discord.Embed(color=embedcolor)
				embed.add_field(name="Clear", value="cleared " + args[1] + " messages")
				embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
				await ctx.send(embed=embed)
			except:
				await ctx.reply("Error, most likely not a number")
	
@bot.command(aliases=['uptime'])
async def ping(ctx):
	current_time = time.time()
	difference = int(round(current_time - start_time))
	uptime = str(datetime.timedelta(seconds=difference))
	embed = discord.Embed(color=embedcolor)
	embed.add_field(name="Ping", value=f'🏓 Pong! {round(bot.latency * 1000)}ms', inline='false')
	embed.add_field(name="Uptime", value=f'{uptime}')
	embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
#	embed.set_timestamp()
	await ctx.reply(embed=embed)
	print('Pinged by '+str(ctx.author))
	

@bot.command()
async def export(ctx, channel):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('🔒'))
		return
	else:
		embed = discord.Embed(color=embedcolor)
		embed.add_field(name="Channel", value=f'{channel}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)
		print('Exported by '+str(ctx.author))

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
		embed = discord.Embed(color=embedcolor, title="Restarting...")
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
		embed = discord.Embed(color=embedcolor, title="Stopping...")
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
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
		embed = discord.Embed(color=embedcolor, description=content)
		await ctx.send(embed=embed)
		print(content+' echoed by '+str(ctx.author))

@bot.command(aliases=['repeat'])
#@bot.check(commands.is_owner())
async def simonsays(ctx, *, content:str=None):
	if not content:
		await ctx.reply("Give me something to say!")
	else:
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
			try:
				m11 = str(ctx.author.nickname)+" asked me politely to say "+content
			except:
				m11 = "somebody forgot to add a message"
			m12 = "I've always wanted to be a simon"
			msg = random.choice([m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12])
			await ctx.reply(str(msg))
			print(content+' echo attempted by '+str(ctx.author))
		else:
			await ctx.message.delete()
			await ctx.send(content)
			print(content+' echoed by '+str(ctx.author))

@bot.command()
async def delete(ctx, messageid):
	if ctx.message.author.id != 545463550802395146:
		await ctx.message.add_reaction(str('❔'))
		return
	else:
		await ctx.message.delete()
		message = await MessageConverter().convert(ctx, messageid)
		await message.delete()
		print('delete attempted by '+str(ctx.author))

@bot.command(aliases=['factoid'])
async def fact(ctx):
	await ctx.message.delete()
	fact = os.popen('curl -s -X GET "https://uselessfacts.jsph.pl/random.txt?language=en" | grep ">" | sed s/\>\ //g').read()
	embed = discord.Embed(color=embedcolor, title="Fact:", description=fact)
	embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
	await ctx.send(embed=embed)
	print("Fact requested by "+ctx.author)

		
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
					logging.error("Bot Broken: \n"+str(error))
					return
				except:
					return
		except:
			return


@bot.event
async def on_message(message):
	await bot.process_commands(message)
	if (message.guild.id == 764981968579461130):
		sentmsg2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+", "+str(message.author)+", "+str(message.content)
		print(sentmsg2)
		with open("logs/test.csv", 'a') as file_object:
			file_object.write(sentmsg2+"\n")

bot.run(token)
