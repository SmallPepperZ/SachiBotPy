import discord
from discord.ext import commands
import json
from mee6_py_api import API




#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)

mee6API = API(302094807046684672)
prefix = configjson["prefix"]
#endregion

fields={}

def addfield(embed, key:str, value:str):
	embed.__setattr__("description", f'{embed.description}\n**{key}:** {value}')
def addrow(embed, value:str):
	embed.__setattr__("description", f'{embed.description}\n{value}')

	

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
	async def add(self, ctx, userid):
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
		invitechannel = self.bot.get_channel(802245295291236442)
		await ctx.reply(f'Adding "{user.name}" to {invitechannel.mention}...')
		try:
			details = await mee6API.levels.get_user_details(userid)
			mclevel = details["level"]
			mcmessages = details["message_count"]
		except TypeError:
			mclevel = "Not enough"
			mcmessages = "Not enough"

		embed = discord.Embed(color=embedcolor, description=f'__**{user.name}#{user.discriminator}**__')
		embed.set_thumbnail(url=user.avatar_url)
		addfield(embed, "Maincord Level", mclevel)
		addfield(embed, "Maincord Messages", mcmessages)
		addfield(embed, "Mention", user.mention)
		addfield(embed, "User ID",  f'`{user.id}`')
		
		await invitechannel.send(embed=embed)


	@invite.command()
	async def update(self, ctx):
		invitechannel = self.bot.get_channel(802245295291236442)
		messages = await invitechannel.history(limit=1).flatten()
		infomsg = await ctx.reply(f"Updating {invitechannel.mention}")
		for message in messages:
			try:
				messagecontents = message.embeds[0]
				splitmessage = messagecontents.description.splitlines()
				l1 = splitmessage[0]
				l2 = splitmessage[1]
				l3 = splitmessage[2]
				l4 = splitmessage[3]
				l5 = splitmessage[4]
				userid = ''.join(x for x in l5 if x.isdigit())
				await infomsg.edit(content=f"Updating {invitechannel.mention}:\n {l1}")
				try:
					details = await mee6API.levels.get_user_details(userid)
					mclevel = details["level"]
					mcmessages = details["message_count"]
				except TypeError:
					mclevel = "Not enough"
					mcmessages = "Not enough"
				embed = discord.Embed(color=embedcolor, description=l1)
				addfield(embed, "Maincord Level", mclevel)
				addfield(embed, "Maincord Messages", mcmessages)
				addrow(embed, l4)
				addrow(embed, l5)
				embed.set_thumbnail(url=messagecontents.thumbnail.url)
				await message.edit(embed=embed)			
			except IndexError:
				return
		await infomsg.edit(content=f"Updating {invitechannel.mention}:\n Completed")		
		
			





def setup(bot):
    bot.add_cog(MdspCog(bot))
