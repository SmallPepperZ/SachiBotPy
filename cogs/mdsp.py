import logging as logger, traceback
import discord
from discord.ext import commands
from discord.ext.commands import BadArgument
import json
import os, sys
from discord.ext.commands import BucketType
from mee6_py_api import API
from datetime import datetime, timedelta, timezone
from tzlocal import get_localzone
import pytz

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)

from customfunctions import checks as customchecks


#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)

mee6API = API(302094807046684672)

invitechannelid = 796109386715758652
invitediscussionchannelid = 792558439863681046
invitechannellimit = 10
prefix = configjson["prefix"]
#endregion

fields={}

def addfield(embed, key:str, value:str):
	embed.__setattr__("description", f'{embed.description}\n**{key}:** {value}')
def addrow(embed, value:str):
	embed.__setattr__("description", f'{embed.description}\n{value}')
def listlines(messagecontents):
	splitmessage = messagecontents.description.splitlines()
	l1 = splitmessage[0]
	l2 = splitmessage[1]
	l3 = splitmessage[2]
	l4 = splitmessage[3]
	l5 = splitmessage[4]
	l6 = splitmessage[5]
	return l1, l2, l3, l4, l5, l6
def getidfrommessage(dictionary:dict, messageid:str):
	for key, value in dictionary.items():
		if messageid == value:
			return key
async def updateinvitestatus(self, ctx, userid, action, force=False):
	if force == "force":
		force = True
	invitechannel = self.bot.get_channel(invitechannelid)
	user = await self.bot.fetch_user(int(userid))		
	infomsg = await ctx.reply(f"Searching for {user.name} in {invitechannel.mention}...")
	
	terms = {
		"approve":{
			"word1": "Approving",
			"word2": f"<:Allowed:786997173845622824> - Approved by {ctx.author.mention}",
			"word3": "approved",
			"color": 0x17820e
		},
		"deny":{
			"word1": "Denying",
			"word2": f"<:Denied:786997173820588073> - Denied by {ctx.author.mention}",
			"word3": "denied",
			"color": 0xa01116
		},
		"pause":{
			"word1": "Pausing",
			"word2": f"⏸️ - Paused by {ctx.author.mention}",
			"word3": "paused",
			"color": 0x444444
		},
		"unpause":{
			"word1": "Unpausing",
			"word2": "None",
			"word3": "unpaused",
			"color": 0xFFFF00
		},
		"accept":{
			"word1": "Accepting",
			"word2": "<:Joined:796147287486627841> - Accepted invite/joined",
			"word3": "changed status to accepted",
			"color": 0x1bc912
		},
		"decline":{
			"word1": "Declining",
			"word2": "<:Leave:796147707709358100> - Invited, but declined",
			"word3": "changed status to declined",
			"color": 0xd81d1a
		}
	}
	word1 = terms[action]["word1"]
	word2 = terms[action]["word2"]
	word3 = terms[action]["word3"]
	color = terms[action]["color"]
	with open('invitees.json', 'r') as file:
		inviteesjson = json.loads(file.read())
	try:
		messageid = inviteesjson[str(userid)]
		logger.debug(messageid)
		message = await self.bot.get_channel(invitechannelid).fetch_message(messageid)
		messagecontents = message.embeds[0]
		splitmessage = messagecontents.description.splitlines()
		l1 = splitmessage[0]
		l2 = splitmessage[1]
		l3 = splitmessage[2]
		l4 = splitmessage[3]
		l5 = splitmessage[4]
		l6 = splitmessage[5]
		roles = [str(role.id) for role in ctx.author.roles]
		if not "None" in l6 and (force == False or not str(796124089294782524) in roles):
			if (action == "accept" or action == "decline"):
				if "<:Allowed:786997173845622824>" in l6:
					null = None			
				else:
					await infomsg.edit(content=f"{action.capitalize()} requires the user to be approved first")
					return
			elif action == "unpause":
				if "⏸️" in l6:
					null = None
				else:
					await infomsg.edit(content=f"{action.capitalize()} requires the user to be paused")
					return
			else:
				await infomsg.edit(content=f"User already has an invite status. Append 'force' to your command if you want to force the status change")
				return
		await infomsg.edit(content=f"{word1} {user.name}...")
		embed = discord.Embed(color=color, description=l1)
		addrow(embed, l2)
		addrow(embed, l3)
		addrow(embed, l4)
		addrow(embed, l5)
		
		addfield(embed, "Invite Status", word2)
		embed.set_thumbnail(url=messagecontents.thumbnail.url)
		if action == "accept":
			invitediscussionchannel = self.bot.get_channel(invitediscussionchannelid) 
			newmsg = await invitediscussionchannel.send(embed=embed)
			await message.delete()
			inviteesjson.pop(str(userid))
			inviteesjson["archive"]["approved"][userid] = newmsg.id
		else:
			await message.edit(embed=embed)	
		await infomsg.edit(content=f"{user.name} successfully {word3}")	
	except:			 
		await infomsg.edit(content=f"{user.name} not found")	
	with open('invitees.json', 'w') as file:
		json.dump(inviteesjson, file, indent=2)



class MdspCog(commands.Cog, name="MDSP"):
	def __init__(self, bot):
		self.bot = bot

	def MDSPOnly():
		def predicate(ctx):
			logger.debug("hi")# a function that takes ctx as it's only arg, that returns a truethy or falsey value, or raises an exception
		return commands.check(predicate)	

	
	@commands.group(aliases=['invitee', 'invitees'])
	@customchecks.limit_to_guild(764981968579461130)
	async def invite(self,ctx):
		if ctx.invoked_subcommand is None:
			delim="\n\n"
			#subcommands = [cmd.name for cmd in ctx.command.commands]
			subcommands = [f'**{cmd.name}:** {cmd.description}' for cmd in ctx.command.commands]
			embed = discord.Embed(color=embedcolor, title="Invite Subcommands:", description=delim.join(list(map(str, subcommands))))
			await ctx.reply(embed=embed)

	@invite.command(description="*Cooldown: 2 minutes*\nAdds a user to #potential-invitees")
	#@commands.cooldown(rate=1, per=120, type=BucketType.user)
	async def add(self, ctx, userid:int):
		try:
			userid = int(userid)
		except ValueError:
			try:
				userid = int("".join([x for x in userid  if x.isdigit()]))
			except ValueError:
				await ctx.reply("Invalid User ID")
		with open('invitees.json', 'r') as file:
			inviteesjson = json.loads(file.read())
		user = await self.bot.fetch_user(int(userid))
		invitechannel = self.bot.get_channel(invitechannelid)
		if (inviteesjson.get(str(userid)) is None) and ctx.guild.get_member(userid) is None:	
			infomsg = await ctx.reply(f'Adding "{user.name}" to {invitechannel.mention}...')
			try:
				details = await mee6API.levels.get_user_details(userid)
				mclevel = details["level"]
				mcmessages = details["message_count"]
			except TypeError:
				mclevel = "Not found, too low?"
				mcmessages = "Not found, too low?"

			embed = discord.Embed(color=0xffff00, description=f'__**{user.name}#{user.discriminator}**__')
			embed.set_thumbnail(url=user.avatar_url)
			addfield(embed, "Maincord Level", mclevel)
			addfield(embed, "Maincord Messages", mcmessages)
			addfield(embed, "Mention", user.mention)
			addfield(embed, "User ID",  f'`{user.id}`')
			addfield(embed, "Invite Status",  f'None')
			await infomsg.edit(content=f'Added "{user.name}" to {invitechannel.mention}')
			message = await invitechannel.send(embed=embed)
		#	await message.add_reaction('<:upvote:771082566752665681>')
		#	await message.add_reaction('<:downvote:771082566651609089>')
			inviteesjson[userid] = message.id
			with open('invitees.json', 'w') as file:
				json.dump(inviteesjson, file, indent=2)
		elif ctx.guild.get_member(userid) is not None:
			await ctx.reply(f'{user.name} is offended that you didn\'t know they were here')
		else:
			await ctx.reply(f'{user.name} already exists in {invitechannel.mention}')

	@invite.command(description="*Cooldown: 5 minutes*\nUpdates maincord message counts, and moves declined/denied users when appropriate")
	@commands.cooldown(rate=1, per=300, type=BucketType.default)
	async def update(self, ctx):
		invitechannel = self.bot.get_channel(invitechannelid)
		invitediscussionchannel = self.bot.get_channel(invitediscussionchannelid) 
		infomsg = await ctx.reply(f"Updating {invitechannel.mention}")
		with open('invitees.json', 'r') as file:
			inviteesjson = json.loads(file.read())
		inviteemessages =  [item for item in inviteesjson["active"].values()]
		messages = [await invitechannel.fetch_message(message) for message in inviteesjson["active"].values()]
		for message in messages:
			messagecontents = message.embeds[0]
			l1, l2, l3, l4, l5, l6 = listlines(messagecontents)
			userid = getidfrommessage(inviteesjson["active"], message.id)
			user = await self.bot.fetch_user(userid)
			sevendaysago = datetime.now(pytz.timezone("UTC")) - timedelta(days=7)
			yesterday = datetime.now(pytz.timezone("UTC")) - timedelta(days=1)
			try:
				lastedited = message.edited_at.replace(tzinfo=pytz.timezone("UTC"))
			except:
				lastedited = message.created_at.replace(tzinfo=pytz.timezone("UTC"))
			logger.debug("Times fetched")
			if (lastedited <= yesterday):
				logger.debug("first if succeeded")
				if ("<:Leave:796147707709358100>" in l6 or "<:Denied:786997173820588073>" in l6) and (lastedited <= sevendaysago):				
					logger.debug("if activated")
					newmsg = await invitediscussionchannel.send(embed=messagecontents)
					await ctx.reply(f'{user.name} moved out of {invitechannel.mention}')
					await message.delete()
					inviteesjson["active"].pop(str(userid))
					inviteesjson["archive"]["denied"][userid] = newmsg.id
					logger.debug("if comopleted")
				else:
					logger.debug("Else activated")
					await infomsg.edit(content=f"Updating {invitechannel.mention}:\n{user.name}")
					logger.debug("infomsg edited")
					try:
						details = await mee6API.levels.get_user_details(userid)
						mclevel = details["level"]
						mcmessages = details["message_count"]
					except TypeError:
						mclevel = "Not found, too low?"
						mcmessages = "Not found, too low?"
					logger.debug("mee6 part done")
					embed = discord.Embed(color=0xffff00, description=l1)
					addfield(embed, "Maincord Level", mclevel)
					addfield(embed, "Maincord Messages", mcmessages)
					addrow(embed, l4)
					addrow(embed, l5)
					addrow(embed, l6)
					embed.set_thumbnail(url=messagecontents.thumbnail.url)
					logger.debug("embed built")
					await message.edit(embed=embed)
					logger.debug("embed sent")
			else:
				logger.debug("User message updated too recently")

			with open('invitees.json', 'w') as file:
				json.dump(inviteesjson, file, indent=2)
			await infomsg.edit(content=f"Updating {invitechannel.mention}:\nCompleted")		
		
			
	@invite.command(description="*Official Helpers Only*\nSets the approved status for a user, and allows `%invite accept` and `%invite decline`")
	@commands.has_role(796124089294782524)
	async def approve(self, ctx, userid:int, force:str=False):		
		await updateinvitestatus(self, ctx, userid, "approve", force)

	@invite.command(description="*Official Helpers Only*\nSets the denied status for a user, and stops other commands from being used on that user, they will be moved to #potential-invitees-discussion after 7ish days")
	@commands.has_role(796124089294782524)
	async def deny(self, ctx, userid:int, force:str=False):		
		await updateinvitestatus(self, ctx, userid, "deny", force)
	
	@invite.command(aliases=['freeze'], description = "*Official Helpers Only*\nSets the paused status for a user, and prevents user from being approved or denied")
	@commands.has_role(796124089294782524)
	async def pause(self, ctx, userid:int, force:str=False):		
		await updateinvitestatus(self, ctx, userid, "pause", force)

	@invite.command(aliases=['unfreeze'], description="*Official Helpers Only*\nResets a user's status from paused")
	@commands.has_role(796124089294782524)
	async def unpause(self, ctx, userid:int, force:str=False):		
		await updateinvitestatus(self, ctx, userid, "unpause", force)

	@invite.command(aliases=['declined', 'leave', 'left'], description="\nUsed by the person who invites a user if they decline the invitation")
	async def decline(self, ctx, userid:int, force:str=False):		
		await updateinvitestatus(self, ctx, userid, "decline", force)

	@invite.command(aliases=['joined', 'accepted', 'join'], description="\nUsed by the person who invites a user if they accept the invitation (or when they join, coming soon™)")
	async def accept(self, ctx, userid:int, force:str=False):		
		await updateinvitestatus(self, ctx, userid, "accept", force)
	
	@add.error
	@approve.error
	@deny.error
	@unpause.error
	@pause.error
	@accept.error
	@decline.error
	@invite.error
	@update.error
	async def invite_cog_error_handler(self, ctx, error):
		if isinstance(error, BadArgument):		
			await ctx.reply(f"Invalid UserID!")
			return
		else:
			await ctx.reply(error)
			exc = error
			etype = type(exc)
			trace = exc.__traceback__

			lines = traceback.format_exception(etype, exc, trace)
			traceback_text = ''.join(lines)
			logger.error(str(traceback_text))
			return


def setup(bot):
	bot.add_cog(MdspCog(bot))
