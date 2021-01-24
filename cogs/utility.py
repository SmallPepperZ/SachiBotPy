import discord
from discord.ext import commands
import json
import time, datetime
from string import ascii_letters, punctuation, whitespace
#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]



#endregion



class UtilityCog(commands.Cog, name="Utility"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['commands'])
	async def help(self, ctx):
		embed = discord.Embed(color=embedcolor, title="Commands")
		embed.add_field(name="__Utilities__", value=ctx.bot.helputility, inline='true')
		embed.add_field(name="__Fun__", value=ctx.bot.helpfun, inline='true')
		if ctx.message.author.id == 545463550802395146:
			embed.add_field(name="__Owner__", value=ctx.bot.helpadmin, inline='false')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)
		print('Help triggered by '+str(ctx.author))

	@commands.command(aliases=['uptime'])
	async def ping(self, ctx):
		current_time = time.time()
		difference = int(round(current_time - ctx.bot.start_time))
		uptime = str(datetime.timedelta(seconds=difference))
		embed = discord.Embed(color=embedcolor)
		embed.add_field(name="Ping", value=f'🏓 Pong! {round(self.bot.latency * 1000)}ms', inline='false')
		embed.add_field(name="Uptime", value=f'{uptime}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)
		print('Pinged by '+str(ctx.author))
	
	@commands.command(aliases=['userinfo'])
	async def whois(self,ctx, userid):
		try:
			userid = ctx.message.mentions[0].id
		except:
			try:
				userid = int(userid)
			except ValueError:
				userid = int("".join([x for x in userid  if x.isdigit()]))
		isguildmember = ctx.guild.get_member(userid) != None
		if isguildmember:
			user = ctx.guild.get_member(userid)
			isadmin = user.guild_permissions.administrator
			nickname = user.display_name
			joindate = user.joined_at
			isowner = ctx.guild.owner.id == user.id
			status = user.status
			ismobile = '\u2705' if user.is_on_mobile() else '\u274E'
			def embedsec1(embed):
				embed.add_field(name="Is the owner?", value=isowner, inline='true')
				embed.add_field(name="Is an admin?", value=isadmin, inline='true')
				embed.add_field(name="Nickname", value=nickname, inline="True")
				embed.add_field(name="Status", value=f'**Status:** {status}\n**Mobile:** {ismobile}', inline="false")
			def embedsec2(embed):
				embed.add_field(name="Join Date", value=joindate, inline='true')
		else:
			print(userid)
			user = await self.bot.fetch_user(int(userid))
			def embedsec1(embed):
				return
			def embedsec2(embed):
				return
		#badges = user.public_flags.all()
		badgelist = {
			"staff": "<:developer:802021494778626080>",
			"partner": "<:partneredserverowner:802021495089004544>",
			"hypesquad": "<:hypesquad:802021494925557791>",
			"bug_hunter": "<:bughunterl1:802021561967575040>",
			"hypesquad_bravery": "<:hypesquadbravery:802021495185473556>",
			"hypesquad_brilliance": "<:hypesquadbrilliance:802021495433461810>",
			"hypesquad_balance": "<:hypesquadbalance:802010940698132490>",
			"early_supporter": "<:earlysupporter:802021494989389885>",
			"bug_hunter_level_2": "<:bughunterl2:802021494975889458>",
			"verified_bot_developer": "<:earlybotdeveloper:802021494875488297>"
		}
		#badgenames = [badge.name for badge in badges]
		#badgeicons = [badgelist[badge] for badge in badgenames]
		delim = " "
		#badgesstr = delim.join(list(map(str, badgeicons)))
		isbot = user.bot
		avatar = user.avatar_url
		createdate = user.created_at
		mention = user.mention
		userid = user.id
		username = user.name+"#"+user.discriminator
		color = user.color
		embed = discord.Embed(color=color,title=username)
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		embed.set_image(url=avatar)
		embed.add_field(name="Is a bot?", value=isbot, inline='true')
		embedsec1(embed)
		embed.add_field(name="Mention", value=mention, inline="False")
		embed.add_field(name="ID", value=f'`{user.id}`', inline="False")
		embed.add_field(name="Account Creation Date", value=createdate, inline='false')
		#if str(badges) != "[]":	
	#		embed.add_field(name="Profile Badges", value=badgesstr, inline='false')
		embedsec2(embed)
		await ctx.send(embed=embed)
		#ctx.guild.get_member(user)




def setup(bot):
    bot.add_cog(UtilityCog(bot))