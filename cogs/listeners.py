import json
import time
import sqlite3 as sl
import logging

import discord
from discord.ext import commands

from customfunctions import config

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


class ListenerCog(commands.Cog, name="Logging"):
	def __init__(self, bot):
		self.bot = bot


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
		if content.startswith(prefix):
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

	@commands.Cog.listener("on_message")
	async def respond_to_pings(self, message:discord.Message):
		pinged        = self.bot.user.mentioned_in(message)
		replied_to    = not("<@796509133985153025>" in message.content or "<@!796509133985153025>" in message.content)
		message_length = len(message.content.split(' '))
		if pinged and not replied_to:
			await message.add_reaction('<:PING:796424651374985266>')
			if message_length == 1:
				await message.reply(f"My prefix is `{prefix}`")
	
	@commands.Cog.listener("on_resumed")
	async def on_resume(self):
		status = config('status')
		await self.bot.change_presence(activity=discord.Activity(type=status[0][1], name=status[1]), status=status[2][1])

def setup(bot):
	bot.add_cog(ListenerCog(bot))
