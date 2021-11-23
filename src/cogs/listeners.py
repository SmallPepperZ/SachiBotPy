
from datetime import datetime
import datetime as dt
import json
import time
import requests 

import discord
from discord.ext import commands, tasks

from utils import config, DBManager, EmbedMaker, StatusManager
from utils import master_logger
# region Variable Stuff


embedcolor = config("embedcolor")
prefix = config("prefix")
heartbeat_url = config("heartbeat")
database = DBManager.Database()
messages_database = DBManager.Database("messages")
logger = master_logger.getChild("listeners")
delete_logger = master_logger.getChild("listeners").getChild("deletions")

# endregion


def get_logging_channel(bot: discord.Client, channel_name: str, guild: int = None) -> discord.TextChannel:
    logging_channels = {
        "joins": lambda: bot.get_channel(database.cursor.execute("SELECT join_channel   FROM log_threads WHERE guild_id=?", (guild,)).fetchone()[0]),
        "invites": lambda: bot.get_channel(database.cursor.execute("SELECT invite_channel FROM log_threads WHERE guild_id=?", (guild,)).fetchone()[0]),
        "java_repost": lambda: bot.get_guild(739176312081743934).get_channel(821778423579410433),
        "bedrock_repost": lambda: bot.get_guild(739176312081743934).get_channel(821778441133097021),
        "servers": lambda: bot.get_guild(797308956162392094).get_channel(867605721424199710)
    }
    database.commit()
    return logging_channels[channel_name]()


def dump_mutes(data: dict) -> None:
    with open("storage/mutes.json", "w") as file:
        json.dump(data, file, indent=2)


async def member_join_update(bot: discord.Client, member: discord.Member, action: str, color) -> None:
    channel = get_logging_channel(bot, "joins", member.guild.id)
    embed = discord.Embed(title=f'User {action.capitalize()}', color=color, description=f"""
	**Guild**
	ID  : `{member.guild.id}`
	Name: [{member.guild.name}](https://discord.com/channels/{member.guild.id})
	**User**
	ID     : `{member.id}`
	Name   : {member.name}
	Mention: {member.mention}
	""")
    await channel.send(embed=embed)


class ListenerCog(commands.Cog, name="Logging"):
    def __init__(self, bot: discord.Client):
        self.bot: discord.Client = bot
        self.sachibotland = bot.get_guild(797308956162392094)
        self.guild_log_guild = bot.get_guild(909148074260168784)
        self.send_heartbeat.start()

    @tasks.loop(minutes=10)
    async def send_heartbeat(self):
        requests.get(heartbeat_url)

    @commands.Cog.listener("on_message")
    async def logmessages(self, message: discord.Message):
        channelignore = [channel[0] for channel in database.cursor.execute(
            "SELECT id from loggingignore where type='channel'")]
        guildignore = [guild[0] for guild in database.cursor.execute(
            "SELECT id from loggingignore where type='guild'")]
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
            messages_database.cursor.execute(sql, sqldata)
            messages_database.commit()
        else:
            return

    @commands.Cog.listener("on_message")
    async def logcommands(self, message: discord.Message):
        content = message.content
        if content.startswith(prefix):
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
            logger.info(
                f'[{guildname}#{channelname}/{message.author}] just executed \'{message.content}\'')
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
            messages_database.cursor.execute(sql, sqldata)
            messages_database.commit()

    @commands.Cog.listener("on_message")
    async def respond_to_pings(self, message: discord.Message):
        pinged = self.bot.user.mentioned_in(message)
        replied_to = not(
            "<@self.bot.user.id>" in message.content or "<@!self.bot.user.id>" in message.content)
        message_length = len(message.content.split(' '))
        if pinged and not replied_to:
            await message.add_reaction('<:PING:796424651374985266>')
            if message_length == 1:
                await message.reply(f"My prefix is `{prefix}`")

    @commands.Cog.listener('on_message')
    async def repost_mc(self, message: discord.Message):
        if message.channel.id == 821778395297349692:
            content = message.content.replace('650159037924769793', '821781958622314576').replace('648530043647033344', '821781958282838069').replace(
                '761566859220221963', '821781958312329237').replace('682276249053429807', '821781958383239188').replace('821162280905211964', '821781958425968650')
            channel_name = "java_repost" if message.content.startswith(
                "**Minecraft: Java Edition") else "bedrock repost"
            channel = get_logging_channel(self.bot, channel_name)
            msg: discord.Message = await channel.send(content)
            await msg.publish()

    @commands.Cog.listener('on_message')
    async def manual_remove_selfmute(self, message: discord.Message):
        if message.guild is None and message.content == "unmute":
            muted_list = self.bot.mutes
            indexes = [i for i, dct in enumerate(
                muted_list) if dct["userid"] == message.author.id]
            if len(indexes) == 0:
                await message.reply("You aren't self-muted anywhere")
            if len(indexes) == 1:
                mute = muted_list[indexes[0]]
                guild: discord.Guild = self.bot.get_guild(mute["guild"])
                muted_role: discord.Role = guild.get_role(mute["role"])
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

    # @commands.Cog.listener('on_message')
    # @commands.Cog.listener('on_resumed')
    # @commands.Cog.listener('on_raw_reaction_add')
    # @commands.Cog.listener('on_raw_reaction_remove')
    # @commands.Cog.listener('on_raw_message_edit')
    # @commands.Cog.listener('on_user_update')
    # async def bot_periodic(self, *_args):
    #     pass

    @commands.Cog.listener("on_resumed")
    async def on_resume(self):
        await StatusManager.apply_status(self.bot)

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        await member_join_update(self.bot, member, "joined", 0x2BDE1F)

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        await member_join_update(self.bot, member, "left", 0xD9361C)

    @commands.Cog.listener("on_raw_message_delete")
    async def message_delete(self, payload: discord.RawMessageDeleteEvent):
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        channel: discord.TextChannel = guild.get_channel(payload.channel_id)
        if payload.cached_message is not None:
            message: discord.Message = payload.cached_message
            delete_logger.debug(
                f"{guild.name:20} | #{channel.name:20} | {payload.message_id:20} | {message.author} | {message.content}")
        else:
            delete_logger.debug(
                f"{guild.name:20} | #{channel.name:20} | {payload.message_id:20}")

    @commands.Cog.listener("on_invite_create")
    async def on_invite_create(self, invite: discord.Invite):
        channel = get_logging_channel(self.bot, "invites", invite.guild.id)
        embed = discord.Embed(title='Invite Created', color=0x2BDE1F, description=f"""
		**Guild**
		ID       : `{invite.guild.id}`
		Name     : [{invite.guild.name}](https://discord.com/channels/{invite.guild.id})
		**Channel**
		ID       : `{invite.channel.id}`
		Name     : [{invite.channel.name}](https://discord.com/channels/{invite.guild.id}/{invite.channel.id})
		Mention  : {invite.channel.mention}
		**Inviter**
		ID       : `{invite.inviter.id}`
		Name     : {invite.inviter}
		Mention  : {invite.inviter.mention}
		**Other**
		Max Time : `{str(dt.timedelta(seconds=invite.max_age))}`
		Max Uses : `{invite.max_uses}`
		Code     : `{invite.code}`
		""")
        await channel.send(embed=embed)

    @commands.Cog.listener("on_invite_delete")
    async def on_invite_delete(self, invite: discord.Invite):
        channel = get_logging_channel(self.bot, "invites", invite.guild.id)
        embed = discord.Embed(title='Invite Deleted', color=0xD9361C, description=f"""
		**Guild**
		ID       : `{invite.guild.id}`
		Name     : [{invite.guild.name}](https://discord.com/channels/{invite.guild.id})
		**Channel**
		ID       : `{invite.channel.id}`
		Name     : [{invite.channel.name}](https://discord.com/channels/{invite.guild.id}/{invite.channel.id})
		Mention  : {invite.channel.mention}
		**Other**
		Code     : `{invite.code}`
		""")
        await channel.send(embed=embed)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS log_threads (
			guild_id       INT PRIMARY KEY NOT NULL,
			log_category   INT             NOT NULL,
			join_channel   INT             NOT NULL,
			invite_channel INT             NOT NULL)""")
        channel = get_logging_channel(self.bot, "servers")

        join_embed = discord.Embed(color=embedcolor, title="Added to guild", description=f"""
		**Guild**
		ID       : `{guild.id}`
		Name     : [{guild.name}](https://discord.com/channels/{guild.id})
		Owner    : {guild.owner.mention}({guild.owner})""")

        owner_in_server = discord.utils.get(
            guild.members, id=self.bot.owner.id) is not None
        
        join_embed.add_field(name="Owner in Guild", value=owner_in_server)
        if owner_in_server:
            await channel.send(embed=join_embed)
        else:
            await channel.send(embed=join_embed, content="Leaving server")
            await guild.leave()

        # Create logging channels if they don't exist 
        if database.cursor.execute("SELECT guild_id from log_threads where guild_id=?", (guild.id,)).fetchone() is None:
            guild_category = await self.guild_log_guild.create_category(name=guild.name, reason=f"Joined {guild.name}")
            invite_channel = await self.guild_log_guild.create_text_channel(name=f'invites', topic=f"Invite logging for {guild.name} ({guild.id}) - <#{guild.system_channel.id}>", reason=f"Joined {guild.name}", category=guild_category)
            join_channel = await self.guild_log_guild.create_text_channel(name=f'joins', topic=f"Join logging for {guild.name} ({guild.id}) - <#{guild.system_channel.id}>", reason=f"Joined {guild.name}", category=guild_category)

            guild_embed = discord.Embed(
                title=f"{guild.name}", color=embedcolor, description="")
            if guild.icon is not None:
                guild_embed.set_thumbnail(url=guild.icon.url)
            EmbedMaker.add_description_field(
                guild_embed, "ID", f"`{guild.id}`")
            EmbedMaker.add_description_field(
                guild_embed, "Name", f"[{guild.name}](https://discord.com/channels/{guild.id})")
            EmbedMaker.add_description_field(
                guild_embed, "Owner", f"{guild.owner}")

            database.cursor.execute("INSERT INTO log_threads (guild_id, log_category, join_channel, invite_channel) values (?,?,?,?)", (
                guild.id, guild_category.id, join_channel.id, invite_channel.id))
            database.commit()

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: discord.Guild):
        channel = get_logging_channel(self.bot, "servers")
        join_embed = discord.Embed(color=embedcolor, title="left guild", description=f"""
		**Guild**
		ID       : `{guild.id}`
		Name     : [{guild.name}](https://discord.com/channels/{guild.id})
		Owner    : {guild.owner.mention}({guild.owner})""")
        await channel.send(embed=join_embed)

    

    async def run_unmutes(self, *_args):
        for index, mute in enumerate(self.bot.mutes.copy()):
            if mute["expiration"] <= datetime.now().timestamp():
                guild = self.bot.get_guild(mute["guild"])
                role = guild.get_role(mute["role"])
                await guild.get_member(mute["userid"]).remove_roles(role, reason="Self mute expiring")
                self.bot.mutes.pop(index)
                dump_mutes(self.bot.mutes)
                break


def setup(bot):
    bot.add_cog(ListenerCog(bot))
