import discord
from discord.embeds import Embed
from discord.ext import commands
import json, logging
import time, datetime
from string import ascii_letters, punctuation, whitespace
from disputils import BotEmbedPaginator
from customfunctions import EmbedMaker

#region Variable Stuff

with open('storage/config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)




#endregion



class UtilityCog(commands.Cog, name="Utility"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx):
		commandsdict = {}
		for cog in self.bot.cogs.keys():
			commandsdict[str(cog)] = {}
		commands = self.bot.walk_commands()
		
		for cmd in commands:
			if (not cmd.hidden) and cmd.enabled:
				
				qname =	cmd.qualified_name
				cog = cmd.cog_name				
				commandsdict[str(cog)][str(qname)] = {
					"description": cmd.description,
					"usage"      : cmd.usage,
					"parent"     : cmd.parent,
					"aliases"    : cmd.aliases,
					"cog"        : cmd.cog_name,
					"signature"  : cmd.signature
					}
		logging.debug("dumping to json finished")
		embed   = discord.Embed(color=embedcolor, title="Help")
		cogdata = ''
		pages   = []
		for cog in commandsdict.keys():
			logging.debug(f"Starting cog loop for {cog}")
			
			for command in commandsdict[cog].keys():
				logging.debug(f"Starting command loop for {cog}")
				signature = f'{commandsdict[cog][command]["signature"]}'
				if commandsdict[cog][command]["description"] != '':
					description = f': {commandsdict[cog][command]["description"]}'
				else:
					description = ''
				cogdata += f'\n`{command} {signature}`{description}'	
			if not cogdata == '':
				if (cog == "Owner" or cog == "Testing"):
					if ctx.author.id == 545463550802395146:
						pages.append(discord.Embed(title=f'Help: {cog}', description=cogdata, color=embedcolor))	
				elif cog == "MDSP":
					if ctx.guild.id == 764981968579461130:
						pages.append(discord.Embed(title=f'Help: {cog}', description=cogdata, color=embedcolor))
				else:
					pages.append(discord.Embed(title=f'Help: {cog}', description=cogdata, color=embedcolor))
			cogdata = ''
			
		paginator = BotEmbedPaginator(ctx, pages)
		await paginator.run()

	@commands.command(aliases=['uptime'])
	async def ping(self, ctx):
		current_time = time.time()
		difference   = int(round(current_time - ctx.bot.start_time))
		uptime       = str(datetime.timedelta(seconds=difference))
		embed        = discord.Embed(color=embedcolor)
		embed.add_field(name="Ping", value=f'🏓 Pong! {round(self.bot.latency * 1000)}ms', inline='false')
		embed.add_field(name="Uptime", value=f'{uptime}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)

	
	@commands.command(aliases=['userinfo'])
	async def whois(self,ctx, userid):
		try:
			userid = ctx.message.mentions[0].id
		except:
			try:
				userid = int(userid)
			except ValueError:
				await ctx.message.add_reaction('<:CommandError:804193351758381086>')
				await ctx.reply("Invalid User ID!", delete_after=10)
				return
		isguildmember = ctx.guild.get_member(userid) != None
		if isguildmember:
			user      = ctx.guild.get_member(userid)
			isadmin   = user.guild_permissions.administrator
			nickname  = user.display_name
			joindate  = user.joined_at
			isowner   = ctx.guild.owner.id == user.id
			status    = user.status
			statusmsg = f' | {user.activity.name}' if user.activity != None else ''
			statuseemojis  = {
				"online" : "🟢",
				"idle"   : "🟡",
				"dnd"    : "🔴",
				"offline": "⚫"
				
			} 
			logging.debug(status)
			if user.is_on_mobile():
				ismobile  = '📱 - '
			elif str(status) != "offline":
				ismobile = '💻 - '
			else:
				ismobile = ""
			statusicon = statuseemojis[str(status)]
			
			def embedsec1(embed):
				EmbedMaker.AddDescriptionField(embed, "Is the owner?", isowner)
				EmbedMaker.AddDescriptionField(embed, "Is an admin?", isadmin)
				EmbedMaker.AddBlankField(embed)
				EmbedMaker.AddDescriptionField(embed, "Status", f'{ismobile}{statusicon}{statusmsg}')
				EmbedMaker.AddBlankField(embed)
			def embedsec2(embed):
				EmbedMaker.AddDescriptionField(embed, "Join Date", joindate)
			def embedsec3(embed):
				EmbedMaker.AddDescriptionField(embed, "Nickname", nickname)
		else:

			user = await self.bot.fetch_user(int(userid))
			def embedsec1(embed):
				return
			def embedsec2(embed):
				return
			def embedsec3(embed):
				return
		flags = user.public_flags.all()
		badgelist = {
			"staff"                 : "<:developer:802021494778626080>",
			"partner"               : "<:partneredserverowner:802021495089004544>",
			"hypesquad"             : "<:hypesquad:802021494925557791>",
			"bug_hunter"            : "<:bughunterl1:802021561967575040>",
			"hypesquad_bravery"     : "<:hypesquadbravery:802021495185473556>",
			"hypesquad_brilliance"  : "<:hypesquadbrilliance:802021495433461810>",
			"hypesquad_balance"     : "<:hypesquadbalance:802010940698132490>",
			"early_supporter"       : "<:earlysupporter:802021494989389885>",
			"bug_hunter_level_2"    : "<:bughunterl2:802021494975889458>",
			"verified_bot_developer": "<:earlybotdeveloper:802021494875488297>"
		}
		flagnames = [flag.name for flag in flags]
		badgeicons = [badgelist[badge] for badge in badgelist if badge in flagnames]
		badgestr   = " ".join(list(map(str, badgeicons)))
		
		isbot      = user.bot
		avatar     = user.avatar_url
		createdate = user.created_at
		mention    = user.mention
		userid     = user.id
		username   = user.name+"#"+user.discriminator
		color      = user.color

		embed       = discord.Embed(color=color,title=username)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		embed.set_image(url=avatar)
		EmbedMaker.AddDescriptionField(embed, "Is a bot?", isbot)
		embedsec1(embed)
		EmbedMaker.AddDescriptionField(embed, "Mention", mention)
		embedsec3(embed)
		EmbedMaker.AddDescriptionField(embed, "User ID", f'`{user.id}`')
		EmbedMaker.AddBlankField(embed)
		EmbedMaker.AddDescriptionField(embed, "Account Creation Date", createdate)
		embedsec2(embed)
		EmbedMaker.AddBlankField(embed)
		if str(badgeicons) != "[]":	
			EmbedMaker.AddDescriptionField(embed, "Profile Badges", badgestr)
		
		await ctx.send(embed=embed)
		#ctx.guild.get_member(user)

	@commands.command(aliases=["online", "areyouthere"])
	async def didyoudie(self, ctx):
		await ctx.reply("I am very much alive", delete_after=20)

def setup(bot):
    bot.add_cog(UtilityCog(bot))