import discord
from discord.ext import commands
import json
import time
import sqlite3 as sl
import logging as logger, logging



#region Variable Stuff

with open('storage/config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
prefix = configjson["prefix"]
dbpath = configjson["logpath"]
dbcon = sl.connect(str(dbpath))
#endregion

with open("storage/loggingignore.json", "r") as loggingignore:
	ignorejson = loggingignore.read()
channelignore = json.loads(ignorejson)["channels"]
guildignore = json.loads(ignorejson)["guilds"]


class LoggerCog(commands.Cog, name="Logging"):
	def __init__(self, bot):
		self.bot = bot

#	@commands.Cog.listener("on_message")
#	async def logmessages(self, message):
#		await self.bot.process_commands(message)
#		if (message.guild.id == 764981968579461130) and (message.channel.id != 789195444957609994) and (message.channel.id != 789607866780745748):
#			sentmsg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+", "+str(message.channel.id)+", "+str(message.channel.name)+", "+str(message.author)+", "+str(message.content)
#			logging.info(f"Message: {sentmsg}")
#			with open("logs/test.csv", 'a') as file_object:
#				file_object.write(sentmsg+"\n")

	@commands.Cog.listener("on_message")
	async def logmessages(self, message):
		try:
			channel = message.channel.id
			channelname = message.channel.name
			guild = message.guild.id
			guildname = message.guild.name
		except AttributeError:
			channel = message.author.id
			channelname = message.author.name
			guild = 0
			guildname = "DM"
		if (not channel in channelignore) and (not guild in guildignore):
			sql = 'INSERT into Messages (created_at, msgid, guildid, channelid, authorid, guildname, channelname, authorname, message, url, attachments) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
			sqldata = [
					int(time.time()), 
					int(message.id),
					int(guild),
					int(channel),
					int(message.author.id),
					str(guildname),
					str(channelname),
					str(message.author),
					str(str(message.system_content)),
					str(message.jump_url),
					str(message.attachments)
						]
			with dbcon:
				dbcon.execute(sql, sqldata)
		else:
			return
	
	@commands.Cog.listener("on_message")
	async def logcommands(self, message):
		
		content = message.content
		if (content.startswith(prefix)):
			try:
				channel     = message.channel.id
				channelname = message.channel.name
				guild       = message.guild.id
				guildname   = message.guild.name
			except AttributeError: 
				channel     = message.author.id
				channelname = message.author.name
				guild       = 0
				guildname   = "DM"
			logger.info(f'{guildname} - {channelname} - {message.author.name} ({message.author.id}) just executed \'{message.content}\'')
			sql = 'INSERT into Commands (created_at, msgid, guildid, channelid, authorid, guildname, channelname, authorname, message, url) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
			sqldata = [
					int(time.time()), 
					int(message.id),
					int(guild),
					int(channel),
					int(message.author.id),
					str(guildname),
					str(channelname),
					str(message.author),
					str(message.content),
					str(message.jump_url)
					   ]
			with dbcon:
				dbcon.execute(sql, sqldata)
			
	# @commands.Cog.listener("on_message")
	# async def spellcheck(self, message):
	# 	if message.channel.id == 806234519258529803 and not message.author.bot:
	# 		corrections = SpellChecker.correct_spelling(message.content)
	# 		if corrections is not None:
	# 			embed = discord.Embed(color=embedcolor, description=f'**Did you mean:**\n{corrections}')
	# 			await message.reply(embed=embed)
				
				
#TODO Add command that admins can use to ignore their server or channel	

def setup(bot):
    bot.add_cog(LoggerCog(bot))
