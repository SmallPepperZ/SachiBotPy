import sqlite3
import logging
import traceback

from datetime import datetime, timedelta

import pytz

import discord
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands import BadArgument, BucketType

from customfunctions.checks import IncorrectGuild
from customfunctions.mee6api import PlayerNotFound
from customfunctions import config, DatabaseFromDict, CustomUtilities, CustomChecks, Mee6Api


logger = logging.getLogger('bot.mdsp')
logg = logging.getLogger()
embedcolor = int(config("embedcolor"), 16)

INVITE_LOG_CHANNEL_ID = 807379254303653939
INVITE_CHANNEL_ID = 796109386715758652
INVITE_DISCUSSION_CHANNEL_ID = 792558439863681046
INVITE_CHANNEL_LIMIT = 10

DB_PATH = "storage/SachiBotStorage.db"
dbcon = sqlite3.connect(str(DB_PATH))
dbcur = dbcon.cursor()


terms = {
	"approve": {
		"word1": "Approving",
		"word2": 'f"<:Allowed:786997173845622824> - Approved by {status_editor_name}"',
		"word3": "approved",
		"color": 0x17820e,
		"name": 'approve'
	},
	"deny": {
		"word1": "Denying",
		"word2": 'f"<:Denied:786997173820588073> - Denied by {status_editor_name}"',
		"word3": "denied",
		"color": 0xa01116,
		"name": 'deny'
	},
	"pause": {
		"word1": "Pausing",
		"word2": 'f"⏸️ - Paused by {status_editor_name}"',
		"word3": "paused",
		"color": 0x444444,
		"name": 'pause'
	},
	"unpause": {
		"word1": "Unpausing",
		"word2": '"None"',
		"word3": "unpaused",
		"color": 0xFFFF00,
		"name": 'none'
	},
	"reset": {
		"word1": "Resetting",
		"word2": '"None"',
		"word3": "reset",
		"color": 0xFFFF00,
		"name": 'none'
	},
	"accept": {
		"word1": "Accepting",
		"word2": '"<:Joined:796147287486627841> - Accepted invite/joined"',
		"word3": "changed status to accepted",
		"color": 0x1bc912,
		"name": 'accept'
	},
	"decline": {
		"word1": "Declining",
		"word2": '"<:Leave:796147707709358100> - Invited, but declined"',
		"word3": "changed status to declined",
		"color": 0xd81d1a,
		"name": 'decline'
	},
	'none': {
		"word2": '"None"',
		"color": 0xFFFF00,
		"name": 'none'
	}
}
fields = {}


def add_field(embed, key: str, value: str):
	embed.__setattr__(
		"description", f'{embed.description}\n**{key}:** {value}')


def add_row(embed, value: str):
	embed.__setattr__("description", f'{embed.description}\n{value}')


async def update_invite_status(self, ctx: commands.Context, userid: int, action: str, force: bool = False):
	invitechannel = self.bot.get_channel(INVITE_CHANNEL_ID)
	user = await self.bot.fetch_user(int(userid))
	infomsg = await ctx.reply(embed=discord.Embed(color=embedcolor, description=f"Searching for {user.name} in {invitechannel.mention}..."))

	status_editor = ctx.author.id
	word1 = terms[action]["word1"]
	word2 = eval(terms[action]["word2"])
	word3 = terms[action]["word3"]
	color = terms[action]["color"]
	# try:
	user_info = dbcon.execute(
		f"""select * from invitees where user_id = {userid}""").fetchone()
	if user_info is None:
		await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"{user.name} not found in {invitechannel.mention}"))
		return

	user_id = user_info[0]
	invite_message_id = user_info[1]
	invite_activity_type = user_info[2]
	field_status = user_info[3]
	field_status_editor = user_info[4]
	field_username = user_info[5]
	field_level = user_info[6]
	field_messages = user_info[7]
	field_mention = user_info[8]
	field_info = user_info[9]
	field_inviter_id = user_info[10]

	messageid: int = invite_message_id
	logger.debug(messageid)
	message = await self.bot.get_channel(INVITE_CHANNEL_ID).fetch_message(messageid)
	messagecontents = message.embeds[0]
	# splitmessage = messagecontents.description.splitlines()
	# l1 = splitmessage[0]
	# l2 = splitmessage[1]
	# l3 = splitmessage[2]
	# l4 = splitmessage[3]
	# l5 = splitmessage[4]
	# l6 = splitmessage[5]
	# try:
	# 	l7 = splitmessage[6]
	# except:
	# 	l7 = ""

	roles = [str(role.id) for role in ctx.author.roles]
	if (field_status != 'none') and (force is False or not (str(765809794732261417) in roles or str(776953964003852309) in roles)):
		if action in ("accept", "decline"):
			if not field_status == "approve":
				await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"{action.capitalize()} requires the user to be approved first"))
				return
		elif action == "unpause":
			if not field_status == "pause":
				await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"{action.capitalize()} requires the user to be paused"))
				return
		else:
			await infomsg.edit(embed=discord.Embed(color=embedcolor, description="User already has an invite status. Use the `--force` flag if you want to force the status change"))
			return

	field_status = terms[action]['name']
	await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"{word1} {user.name}..."))
	embed = discord.Embed(color=color, description=f'__**{field_username}**__')
	status_editor_name = ctx.author.mention
	add_field(embed, "Maincord Level", field_level)
	add_field(embed, "Maincord Messages", field_messages)
	add_field(embed, "Mention", user.mention)
	add_field(embed, "User ID",  f'`{user.id}`')
	add_field(embed, "Invite Status", f'{eval(terms[field_status]["word2"])}')
	add_field(embed, "Info", field_info)
	embed.set_thumbnail(url=user.avatar_url)
	footer = messagecontents.footer
	embed.set_footer(text=footer.text, icon_url=footer.icon_url)
	db_data_dict = {
		'user_id': user.id,
		'invite_message_id': message.id,
		'invite_activity_type': invite_activity_type,
		'field_status': field_status,
		'field_status_editor': status_editor,
		'field_username': f'{user.name}#{user.discriminator}',
		'field_level': field_level,
		'field_messages': field_messages,
		'field_mention': field_mention,
		'field_info': field_info,
		'field_inviter_id': field_inviter_id,
	}

	values = tuple(db_data_dict.values())
	footer = messagecontents.footer
	embed.set_footer(text=footer.text, icon_url=footer.icon_url)
	sql = DatabaseFromDict.make_placeholder('invitees', db_data_dict)
	dbcon.execute(sql, values)
	dbcon.commit()

	logembed = discord.Embed(color=embedcolor,
							 title="Invitee edited", description="")
	logembed.set_author(name=ctx.author.name,
						url=ctx.message.jump_url,
						icon_url=ctx.author.avatar_url)
	logembed.set_thumbnail(url=user.avatar_url)

	embed.set_thumbnail(url=user.avatar_url)
	if action == "accept":
		invitediscussionchannel = self.bot.get_channel(
			INVITE_DISCUSSION_CHANNEL_ID)
		newmsg = await invitediscussionchannel.send(embed=embed)
		add_field(logembed, "User edited", f'[{user.name}]({newmsg.jump_url})')
		await message.delete()
		sql = f"""update invitees set invite_activity_type = 'approved', invite_message_id = {newmsg.id} where user_id = {userid}"""
		dbcon.execute(sql)
		dbcon.commit()
	else:
		await message.edit(embed=embed)
		add_field(logembed, "User edited",
				  f'[{user.name}]({message.jump_url})')
	await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"{user.name} successfully {word3}"))

	await self.bot.get_channel(INVITE_LOG_CHANNEL_ID).send(embed=logembed)
	# except:
	#	await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"{user.name} not found")	)


class MdspCog(commands.Cog, name="MDSP"):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener("on_message")
	async def auto_delete(self, message: discord.Message):
		try:
			guild_id = message.guild.id
		except:
			guild_id = None
		if guild_id == 764981968579461130 and '@everyone' in message.content and not '`@everyone' in message.content and not message.mention_everyone:
			await message.delete()
			embed = discord.Embed(
				description=f'{message.author.display_name} just used `@ everyone`')
			logchannel = self.bot.get_channel(807379254303653939)
			await logchannel.send(embed=embed)

	@commands.group(aliases=['invitee', 'invitees'])
	@CustomChecks.limit_to_guild(764981968579461130)
	async def invite(self, ctx):
		if ctx.invoked_subcommand is None:
			delim = "\n\n"
			#subcommands = [cmd.name for cmd in ctx.command.commands]
			subcommands = [
				f'**{cmd.name}:** {cmd.description}' for cmd in ctx.command.commands]
			embed = discord.Embed(color=embedcolor, title="Invite Subcommands:",
								  description=delim.join(list(map(str, subcommands))))
			await ctx.reply(embed=embed)

	@invite.command(description="*Cooldown: 2 minutes*\nAdds a user to #potential-invitees")
	# @commands.cooldown(rate=1, per=120, type=BucketType.user)
	async def add(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		if len(args) > 1:
			info = args[1:]
		else:
			info = ''

		try:
			userid = int(userid)
		except ValueError:
			try:
				userid = int("".join([x for x in list(userid) if x.isdigit()]))
			except ValueError:
				await ctx.reply("Invalid User ID")

		user = await self.bot.fetch_user(int(userid))
		invitechannel = self.bot.get_channel(INVITE_CHANNEL_ID)
		not_in_db = dbcon.execute(
			f'''select * from invitees where user_id = {userid}''').fetchone() is None
		if (not_in_db) and ctx.guild.get_member(userid) is None:
			infomsg = await ctx.reply(embed=discord.Embed(color=embedcolor, description=f'Adding "{user.name}" to {invitechannel.mention}...'))
			try:
				mc_level, mc_messages = Mee6Api.get_user(
					userid, pages=10, limit=1000)
				ironminer = bool(mc_level >= 10 or force)
			except PlayerNotFound:
				mc_level = "Not found, too low?"
				mc_messages = "Not found, too low?"
				ironminer = False

			if ironminer:
				embed = discord.Embed(
					color=0xffff00, description=f'__**{user.name}#{user.discriminator}**__')
				embed.set_thumbnail(url=user.avatar_url)
				add_field(embed, "Maincord Level", mc_level)
				add_field(embed, "Maincord Messages", mc_messages)
				add_field(embed, "Mention", user.mention)
				add_field(embed, "User ID",  f'`{user.id}`')
				add_field(embed, "Invite Status",  'None')
				add_field(embed, "Info",  info)
				embed.set_footer(
					text=f'Suggested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
				await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f'Added "{user.name}" to {invitechannel.mention}'))
				message = await invitechannel.send(embed=embed)
				#	await message.add_reaction('<:upvote:771082566752665681>')
				#	await message.add_reaction('<:downvote:771082566651609089>')

				db_data_dict = {
					'user_id': user.id,
					'invite_message_id': message.id,
					'invite_activity_type': 'active',
					'field_status': 'none',
					'field_status_editor': None,
					'field_username': f'{user.name}#{user.discriminator}',
					'field_level': mc_level,
					'field_messages': mc_messages,
					'field_mention': user.mention,
					'field_info': info,
					'field_inviter_id': ctx.author.id,
				}
				values = tuple(db_data_dict.values())
				sql = DatabaseFromDict.make_placeholder(
					'invitees', db_data_dict)
				dbcur.execute(sql, values)
				dbcon.commit()
				logembed = discord.Embed(
					color=embedcolor,      title="Invitee added")
				logembed.set_author(
					name=ctx.author.name, url=ctx.message.jump_url, icon_url=ctx.author.avatar_url)
				add_field(logembed, "User added",
						  f'[{user.name}]({message.jump_url})')
				logembed.set_thumbnail(url=user.avatar_url)
				await self.bot.get_channel(INVITE_LOG_CHANNEL_ID).send(embed=logembed)

			else:
				await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f'''{user.name} is not yet an iron miner, try to add them again when they are ||(or maybe the api isn't working)||'''))
		elif ctx.guild.get_member(userid) is not None:
			await ctx.reply(f'{user.name} is offended that you didn\'t know they were here')
		else:
			await ctx.reply(f'{user.name} already exists in {invitechannel.mention}')

	@invite.command(description="*Cooldown: 1 hour*\nUpdates maincord message counts, and moves declined/denied users when appropriate")
	@commands.cooldown(rate=1, per=3600, type=BucketType.default)
	async def update(self, ctx:discord.ext.commands.Context):
		invitechannel = self.bot.get_channel(INVITE_CHANNEL_ID)
		invitediscussionchannel = self.bot.get_channel(
			INVITE_DISCUSSION_CHANNEL_ID)
		infomsg = await ctx.reply(embed=discord.Embed(color=embedcolor, description=f"Updating {invitechannel.mention}"))
		invitee_info_list = []

		message_id_query = dbcon.execute(
			"""select invite_message_id from invitees where invite_activity_type = 'active'""")
		message_id_tuples = message_id_query.fetchall()
		message_ids = [id[0] for id in message_id_tuples]
		messages = [await invitechannel.fetch_message(message) for message in message_ids]
		for message in messages:
			messagecontents = message.embeds[0]
			#l1, l2, l3, l4, l5, l6, l7 = list_lines(messagecontents)
			user_info = dbcon.execute(
				f"""select * from invitees where invite_message_id = {message.id}""").fetchone()

			user_id = user_info[0]
			invite_message_id = user_info[1]
			invite_activity_type = user_info[2]
			field_status = user_info[3]
			field_status_editor = user_info[4]
			field_username = user_info[5]
			field_level = user_info[6]
			field_messages = user_info[7]
			field_mention = user_info[8]
			field_info = user_info[9]
			field_inviter_id = user_info[10]

			user = await self.bot.fetch_user(user_id)
			sevendaysago = datetime.now(
				pytz.timezone("UTC")) - timedelta(days=7)
			yesterday = datetime.now(pytz.timezone("UTC")) - timedelta(days=1)
			try:
				lastedited = message.edited_at.replace(
					tzinfo=pytz.timezone("UTC"))
			except:
				lastedited = message.created_at.replace(
					tzinfo=pytz.timezone("UTC"))
			logger.debug(field_status)

			if (field_status in ('decline', 'deny')) and (lastedited <= sevendaysago):
				logger.debug("if activated")
				newmsg = await invitediscussionchannel.send(embed=messagecontents)
				await ctx.reply(f'{user.name} moved out of {invitechannel.mention}')
				await message.delete()
				sql = f"""update invitees set invite_activity_type = 'denied', invite_message_id = {newmsg.id} where user_id = {user_id}"""
				dbcon.execute(sql)
				dbcon.commit()
				logger.debug("if completed")
			else:

				await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"Updating {invitechannel.mention}:\n{user.name}"))

				try:
					mc_level, mc_messages = Mee6Api.get_user(
						user_id, pages=10, limit=1000)
				except PlayerNotFound:
					mc_level = "Not found, too low?"
					mc_messages = "Not found, too low?"
				logger.debug("Got Mee6 info")
				# Remake embed
				embed = discord.Embed(color=terms[field_status]["color"],
									  description=f'__**{field_username}**__')
				# add_field(embed, "Maincord Level", mc_level)
				# add_field(embed, "Maincord Messages", mc_messages)
				# add_row(embed, l4)
				# add_row(embed, l5)
				# add_row(embed, l6)
				# add_row(embed, l7)
				status_editor_name = ctx.guild.get_member(field_status_editor).display_name
				add_field(embed, "Maincord Level", mc_level)
				add_field(embed, "Maincord Messages", mc_messages)
				add_field(embed, "Mention", user.mention)
				add_field(embed, "User ID",  f'`{user.id}`')
				add_field(embed, "Invite Status", f'{eval(terms[field_status]["word2"])}')
				add_field(embed, "Info", field_info)
				embed.set_thumbnail(url=user.avatar_url)
				footer = messagecontents.footer
				embed.set_footer(text=footer.text, icon_url=footer.icon_url)
				db_data_dict = {
					'user_id': user.id,
					'invite_message_id': message.id,
					'invite_activity_type': invite_activity_type,
					'field_status': field_status,
					'field_status_editor': field_status_editor,
					'field_username': f'{user.name}#{user.discriminator}',
					'field_level': mc_level,
					'field_messages': mc_messages,
					'field_mention': field_mention,
					'field_info': field_info,
					'field_inviter_id': field_inviter_id,
				}

				values = tuple(db_data_dict.values())
				invitee_info_list.append(values)

				# Send embed
				await message.edit(embed=embed)
		logger.debug("Update completed")
		sql = DatabaseFromDict.make_placeholder('invitees', db_data_dict)
		dbcon.executemany(sql, invitee_info_list)
		dbcon.commit()
		await infomsg.edit(embed=discord.Embed(color=embedcolor, description=f"Updating {invitechannel.mention}:\nCompleted"))

	@invite.command(description="*Official Helpers Only*\nSets the approved status for a user, and allows `%invite accept` and `%invite decline`")
	@commands.has_any_role(776953964003852309, 765809794732261417, 770135456724680704)
	async def approve(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		await update_invite_status(self, ctx, userid, "approve", force)

	@invite.command(description="*Official Helpers Only*\nSets the denied status for a user, and stops other commands from being used on that user, they will be moved to #potential-invitees-discussion after 7ish days")
	@commands.has_any_role(776953964003852309, 765809794732261417, 770135456724680704)
	async def deny(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		await update_invite_status(self, ctx, userid, "deny", force)

	@invite.command(aliases=['freeze'], description="*Official Helpers Only*\nSets the paused status for a user, and prevents user from being approved or denied")
	@commands.has_any_role(776953964003852309, 765809794732261417, 770135456724680704)
	async def pause(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		await update_invite_status(self, ctx, userid, "pause", force)

	@invite.command(aliases=['unfreeze'], description="*Official Helpers Only*\nResets a user's status from paused")
	@commands.has_any_role(776953964003852309, 765809794732261417, 770135456724680704)
	async def unpause(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		await update_invite_status(self, ctx, userid, "unpause", force)

	@invite.command(aliases=['declined', 'leave', 'left'], description="\nUsed by the person who invites a user if they decline the invitation")
	async def decline(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		await update_invite_status(self, ctx, userid, "decline", force)

	@invite.command(aliases=['joined', 'accepted', 'join'], description="\nUsed by the person who invites a user if they accept the invitation (or when they join, coming soon™)")
	async def accept(self, ctx, *args):
		flags = ['-f', '--force']
		force = False
		usedflags, args = CustomUtilities.find_flags(flags, args)
		userid = int(args[0])
		for flag in flags:
			if flag in usedflags:
				force = True
		await update_invite_status(self, ctx, userid, "accept", force)

	@invite.command(aliases=['unset'], description="*Official Helpers Only*\nResets a user's status")
	@commands.has_any_role(776953964003852309, 765809794732261417, 770135456724680704)
	async def reset(self, ctx, userid: int):
		await update_invite_status(self, ctx, userid, "unpause", True)

	@invite.command()
	@commands.is_owner()
	async def errorme(self, ctx):
		await ctx.reply(0/0)

	@add.error
	@approve.error
	@deny.error
	@unpause.error
	@pause.error
	@accept.error
	@decline.error
	@invite.error
	@update.error
	@errorme.error
	async def invite_cog_error_handler(self, ctx, error):
		if isinstance(error, BadArgument):
			await ctx.reply("Invalid UserID!")
			return
		elif isinstance(error, NotFound):
			await ctx.reply('User could not be found')
			return
		elif isinstance(error, IncorrectGuild):
			await ctx.reply('This command is limited to a different guild')
		else:
			exc = error
			error_type = type(exc)
			trace = exc.__traceback__

			lines = traceback.format_exception(error_type, exc, trace)
			traceback_text = ''.join(lines)
			await ctx.reply(f'Error:  \n```{error}```')
			logger.error(str(traceback_text))
			return


def setup(bot):
	bot.add_cog(MdspCog(bot))
