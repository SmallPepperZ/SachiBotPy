import discord; from discord.ext import commands
import json
import time
import sqlite3 as sl
from customfunctions import config
import logging


#region Variable Stuff


embedcolor = int(config("embedcolor"), 16)
prefix = config("prefix")
db_path = "storage/DiscordMessages.db"
dbcon = sl.connect(str(db_path))
logger = logging.getLogger("bot.logging")
#endregion

with open("storage/loggingignore.json", "r") as loggingignore:
	ignore_json = loggingignore.read()
channelignore = json.loads(ignore_json)["channels"]
guildignore   = json.loads(ignore_json)["guilds"]


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
	async def logmessages(self, message:discord.Message):
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
			
				
				
#TODO Add command that admins can use to ignore their server or channel	

def setup(bot):
    bot.add_cog(LoggerCog(bot))
