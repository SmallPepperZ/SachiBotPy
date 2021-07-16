import datetime

import discord
from discord.ext import commands
from customfunctions import config
from customfunctions import master_logger

# region Variable Stuff

logger = master_logger.getChild("testing")
embedcolor = config("embedcolor")

# endregion



class TestingCog(commands.Cog, name="Testing"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@commands.command()
	@commands.cooldown(rate=1, per=300)
	@commands.is_owner()
	async def changeinvitehelp(self, ctx, *, contents):
		channel = self.bot.get_channel(792558439863681046)
		message = await channel.fetch_message(804147923285573633)
		embed = discord.Embed(color=embedcolor, description=contents)
		await message.edit(embed=embed)
		await ctx.message.add_reaction('✅')

	@commands.command()
	@commands.is_owner()
	async def inviteurltester(self, ctx, userid:int):
		user = self.bot.get_user(int(userid))
		try:
			username=user.name
		except AttributeError:
			username="Unknown User"
		channel = ctx.guild.get_channel(797308957478879234)
		invite = await channel.create_invite(reason=f"Invite for {username}", max_uses=1,unique=True, max_age=604800)
		await ctx.send(invite.url)

	@commands.command(enabled=True)
	@commands.is_owner()
	async def errorme(self, ctx, err_type:str="div"):
		if err_type == "div":
			logger.debug(0/0)
		elif err_type == "del":
			await ctx.message.delete()
			await ctx.send("hi")
		else:
			raise ValueError



	@commands.command()
	@commands.is_owner()
	async def auditlog(self, ctx,*_,guild:discord.Guild=None, action:discord.AuditLogAction=None,limit:int=1000, user:discord.User=None, target:discord.User=None):
		guild = guild if guild is not None else ctx.guild
		async for entry in guild.audit_logs(action=action, limit=limit, user=user):
			if target is not None and entry.target.id != target.id:
				continue
			entry:discord.AuditLogEntry = entry
			await ctx.send(f'{entry.created_at} | {entry.user} | {entry.before} | {entry.after} | {entry.target}')



	@commands.command()
	@commands.is_owner()
	async def msg_count(self,ctx,channel,date_range:int=5):
		channel:discord.TextChannel=await self.bot.fetch_channel(channel)
		today = datetime.datetime.today()
		for i in range(date_range):
			start_day = today - datetime.timedelta(days=(i+1))
			end_day = today - datetime.timedelta(days=i)
			history:"list[discord.Message]" = await channel.history(limit=20000,after=start_day,before=end_day).flatten()
			await ctx.send(history[0].jump_url+"\n"+history[-1].jump_url)

def setup(bot):
	bot.add_cog(TestingCog(bot))
