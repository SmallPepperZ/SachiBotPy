from datetime import datetime
import json
import time
import sqlite3 as sl
import logging

import discord
from discord.ext import commands

from customfunctions import config

#region Variable Stuff

def get_logging_channel(bot:discord.Client,channel_name:str) -> discord.TextChannel:
	logging_channels = {
	"joins": lambda: bot.get_guild(797308956162392094).get_channel(844600626516328519),
	"invites": lambda: bot.get_guild(797308956162392094).get_channel(845350291103809546)
	}
	return logging_channels[channel_name]


embedcolor = int(config("embedcolor"), 16)
prefix = config("prefix")
DB_PATH = "storage/DiscordMessages.db"
dbcon = sl.connect(str(DB_PATH))
logger = logging.getLogger("bot.logging")
#endregion

with open("storage/loggingignore.json", "r") as loggingignore:
	ignore_json = loggingignore.read()
channelignore = json.loads(ignore_json)["channels"]
guildignore   = json.loads(ignore_json)["guilds"]

def dump_mutes(data:dict) -> None:
	with open("storage/mutes.json", "w") as file:
		json.dump(data, file, indent=2)

async def member_join_update(bot:discord.Client, member:discord.Member, action:str, color) -> None:
	channel = get_logging_channel(bot, "joins")
	embed = discord.Embed(title=f'User {action.capitalize()}',color=color, description=f"""
	**Guild**
	ID  : `{member.guild.id}`
	Name: {member.guild.name}
	**User**
	ID     : `{member.id}`
	Name   : {member.name}
	Mention: {member.mention}
	""")
	await channel.send(embed=embed)
class ListenerCog(commands.Cog, name="Logging"):
	def __init__(self, bot):
		self.bot:discord.Client = bot


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

	@commands.Cog.listener('on_message')
	async def repost_mc(self, message:discord.Message):
		if message.channel.id == 821778395297349692:
			channel_id = None
			if message.content.startswith("**Minecraft: Java Edition"):
				channel_id = 821778423579410433
			elif message.content.startswith("**Minecraft: Bedrock Edition"):
				channel_id = 821778441133097021
			if channel_id is not None:
				content = message.content.replace('650159037924769793', '821781958622314576').replace('648530043647033344', '821781958282838069').replace('761566859220221963', '821781958312329237').replace('682276249053429807', '821781958383239188').replace('821162280905211964','821781958425968650')
				channel = self.bot.get_channel(channel_id)
				msg:discord.Message = await channel.send(content)
				await msg.publish()

	@commands.Cog.listener('on_message')
	async def manual_remove_selfmute(self, message:discord.Message):
		if message.guild is None and message.content == "unmute":
			print(message.author.id)
			muted_list = self.bot.mutes
			indexes = [i for i,dct in enumerate(muted_list) if dct["userid"] == message.author.id]
			if len (indexes) == 0:
				await message.reply("You aren't self-muted anywhere")
			if len (indexes) == 1:
				mute = muted_list[indexes[0]]
				guild:discord.Guild = self.bot.get_guild(mute["guild"])
				muted_role:discord.Role = guild.get_role(mute["role"])
				await guild.get_member(message.author.id).remove_roles(muted_role, reason="Self mute manually removed")
				self.bot.mutes.pop(indexes[0])
				dump_mutes(self.bot.mutes)
				await message.reply(f"Unmuting you in {guild.name}")
			else:
				await message.reply("You are selfmuted in more than one place, and I haven't added code to account for that")
			# else: #If user is self-muted in more than one server
			# 	server_list = {}
			# 	for mute in mutes:
			# 		guild = self.bot.get_guild(mute["guild"])
			# 		server_list[guild.id]=guild.name
			# 	await message.reply("You are self-muted in the following servers. Enter the id of the one you would like to revoke\n"+'\n'.join([f'{guild_id} | {guild_name}' for guild_id, guild_name in server_list.items()])) # Prompt with available guilds

			# 	def guild_check(message):
			# 		return message.content in server_list.keys() or message.content in server_list.values() # Make sure response is valid

			# 	try:
			# 		selected_guild = (await self.bot.wait_for('message', check=guild_check,timeout=60.0)).content # Ask for which guild to use
			# 	except asyncio.TimeoutError:
			# 		await message.reply("Timed out")
			# 		return
			# 	mute = [mute for mute in mutes if selected_guild in (mute["guild"],server_list[mute["guild"]])][0]
			# 	guild:discord.Guild = self.bot.get_guild(mute["guild"])
			# 	muted_role:discord.Role = guild.get_role(mute["role"])
			# 	await guild.get_member(message.author.id).remove_roles(muted_role, reason="Self mute manually removed")
			# 	self.bot.mutes.pop(indexes[0])
			# 	dump_mutes(self.bot.mutes)


	@commands.Cog.listener('on_message')
	@commands.Cog.listener('on_resumed')
	@commands.Cog.listener('on_raw_reaction_add')
	@commands.Cog.listener('on_raw_reaction_remove')
	@commands.Cog.listener('on_raw_message_edit')
	@commands.Cog.listener('on_user_update')
	async def run_unmutes(self, *_args):
		for index, mute in enumerate(self.bot.mutes.copy()):
			print(mute)
			if mute["expiration"] <= datetime.now().timestamp():
				print("Expired mute!")
				guild = self.bot.get_guild(mute["guild"])
				role = guild.get_role(mute["role"])
				await guild.get_member(mute["userid"]).remove_roles(role, reason="Self mute expiring")
				self.bot.mutes.pop(index)
				dump_mutes(self.bot.mutes)
				break




	@commands.Cog.listener("on_resumed")
	async def on_resume(self):
		status = config('status')
		await self.bot.change_presence(activity=discord.Activity(type=status[0][1], name=status[1]), status=status[2][1])

	@commands.Cog.listener("on_member_join")
	async def on_member_join(self, member: discord.Member):
		await member_join_update(self.bot, member, "joined", 0x2BDE1F)

	@commands.Cog.listener("on_member_leave")
	async def on_member_remove(self, member: discord.Member):
		await member_join_update(self.bot, member, "left", 0xD9361C)



def setup(bot):
	bot.add_cog(ListenerCog(bot))
