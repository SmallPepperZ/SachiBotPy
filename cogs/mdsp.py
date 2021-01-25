import discord
from discord.ext import commands
from discord.ext.commands import BadArgument
import json
from discord.ext.commands import BucketType
from mee6_py_api import API



#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)

mee6API = API(302094807046684672)

invitechannelid = 802245295291236442
invitechannellimit = 1
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

async def updateinvitestatus(self, ctx, userid, action):
	invitechannel = self.bot.get_channel(invitechannelid)
	user = await self.bot.fetch_user(int(userid))		
	messages = await invitechannel.history(limit=invitechannellimit).flatten()
	infomsg = await ctx.reply(f"Searching for {user.name} in {invitechannel.mention}...")
	
	terms = {
		"approve":{
			"word1": "Approving",
			"word2": f"<:Allowed:786997173845622824> - Approved by {ctx.author.mention}",
			"word3": "approved",
			"color": 0x00FF00
		},
		"deny":{
			"word1": "Denying",
			"word2": f"<:Denied:786997173820588073> - Denied by {ctx.author.mention}",
			"word3": "denied",
			"color": 0xFF0000
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
			"color": 0x444444
		}
	}
	word1 = terms[action]["word1"]
	word2 = terms[action]["word2"]
	word3 = terms[action]["word3"]
	color = terms[action]["color"]
	for message in messages:	
		try:
			messagecontents = message.embeds[0]
			splitmessage = messagecontents.description.splitlines()
			l1 = splitmessage[0]
			l2 = splitmessage[1]
			l3 = splitmessage[2]
			l4 = splitmessage[3]
			l5 = splitmessage[4]
			l6 = splitmessage[5]
			if l1 == f'__**{user.name}#{user.discriminator}**__':		
				await infomsg.edit(content=f"{word1} {user.name}...")
				embed = discord.Embed(color=color, description=l1)
				addrow(embed, l2)
				addrow(embed, l3)
				addrow(embed, l4)
				addrow(embed, l5)
				
				addfield(embed, "Invite Status", word2)
				embed.set_thumbnail(url=messagecontents.thumbnail.url)
				await message.edit(embed=embed)			
			else:
				return
		except IndexError:
			await ctx.reply(f'{user.name} not found in {invitechannel.mention}')
	await infomsg.edit(content=f"{user.name} successfully {word3}")	
	

class MdspCog(commands.Cog, name="MDSP"):
	def __init__(self, bot):
		self.bot = bot


	@commands.group()
	async def invite(self,ctx):
		if ctx.invoked_subcommand is None:
			delim=", "
			subcommands = [cmd.name for cmd in ctx.command.commands]
			await ctx.send(f'Please select one of the subcommands ({delim.join(list(map(str, subcommands)))})')

	@invite.command()
	@commands.cooldown(rate=1, per=120, type=BucketType.user)
	async def add(self, ctx, userid:int):
		try:
			userid = ctx.message.mentions[0].id
		except:
			try:
				userid = int(userid)
			except ValueError:
				try:
					userid = int("".join([x for x in userid  if x.isdigit()]))
				except ValueError:
					await ctx.reply("Invalid User ID")
		 
		user = await self.bot.fetch_user(int(userid))
		invitechannel = self.bot.get_channel(invitechannelid)
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
		await invitechannel.send(embed=embed)


	@invite.command()
	@commands.cooldown(rate=1, per=300, type=BucketType.default)
	async def update(self, ctx):
		invitechannel = self.bot.get_channel(invitechannelid)
		messages = await invitechannel.history(limit=invitechannellimit).flatten() 
		infomsg = await ctx.reply(f"Updating {invitechannel.mention}")
		for message in messages:
			try:
				messagecontents = message.embeds[0]
				l1, l2, l3, l4, l5, l6 = listlines(messagecontents)
				
					
				userid = ''.join(x for x in l5 if x.isdigit())
				await infomsg.edit(content=f"Updating {invitechannel.mention}:\n {l1}")
				try:
					details = await mee6API.levels.get_user_details(userid)
					mclevel = details["level"]
					mcmessages = details["message_count"]
				except TypeError:
					mclevel = "Not found, too low?"
					mcmessages = "Not found, too low?"
				embed = discord.Embed(color=0xffff00, description=l1)
				addfield(embed, "Maincord Level", mclevel)
				addfield(embed, "Maincord Messages", mcmessages)
				addrow(embed, l4)
				addrow(embed, l5)
				addrow(embed, l6)
				embed.set_thumbnail(url=messagecontents.thumbnail.url)
				await message.edit(embed=embed)			
			except IndexError:
				return
		await infomsg.edit(content=f"Updating {invitechannel.mention}:\n Completed")		
		
			
	@invite.command()
	@commands.has_role(796124089294782524)
	async def approve(self, ctx, userid:int):		
		await updateinvitestatus(self, ctx, userid, "approve")

	@invite.command()
	@commands.has_role(796124089294782524)
	async def deny(self, ctx, userid:int):		
		await updateinvitestatus(self, ctx, userid, "deny")
	
	@invite.command(aliases=['freeze'])
	@commands.has_role(796124089294782524)
	async def pause(self, ctx, userid:int):		
		await updateinvitestatus(self, ctx, userid, "pause")

	@invite.command(aliases=['unfreeze'])
	@commands.has_role(796124089294782524)
	async def unpause(self, ctx, userid:int):		
		await updateinvitestatus(self, ctx, userid, "unpause")
	
	@add.error
	@approve.error
	@deny.error
	@unpause.error
	@pause.error
	async def invite_cog_error_handler(self, ctx, error):
		if isinstance(error, BadArgument):		
			await ctx.reply(f"Invalid UserID!")
			return


def setup(bot):
    bot.add_cog(MdspCog(bot))
