import discord
from discord.ext import commands
import json
import time, datetime
import os, sys

from discord.ext.commands.errors import ExtensionNotLoaded
from discord.ext.commands.errors import ExtensionFailed

#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]
#endregion



class OwnerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def restart(self, ctx):
		await ctx.message.delete()
		current_time = time.time()
		start_time = ctx.bot.start_time
		difference = int(round(current_time - start_time))
		uptime = str(datetime.timedelta(seconds=difference))
		embed = discord.Embed(color=embedcolor, title="Restarting...")
		embed.set_footer(text=f"lasted for {uptime}")
		await ctx.send(embed=embed)
		print('Bot restarted by '+str(ctx.author))
		await os.system("pm2 restart 0")
		await self.bot.logout()
		sys.exit(0)

	@commands.command()
	@commands.is_owner()
	async def stop(self, ctx):
		await ctx.message.delete()
		embed = discord.Embed(color=embedcolor, title="Stopping...")
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.send(embed=embed)
		print('Bot stopped by '+str(ctx.author))
		await os.system("pm2 stop 0")
		await self.bot.logout()

	@commands.command()
	@commands.is_owner()
	async def export(self, ctx, channel):
		embed = discord.Embed(color=embedcolor)
		embed.add_field(name="Channel", value=f'{channel}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
		await ctx.reply(embed=embed)
		print('Exported by '+str(ctx.author))

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, cog):
		cogs = str(ctx.bot.coglist)
		cognames = cogs.replace('cogs.', '').replace('[', '').replace(']', '').replace("\'", "").replace(",", "\n")
		try:
			self.bot.reload_extension(f'cogs.{cog}')
			embed = discord.Embed(color=embedcolor, title="Reloading Cog...")
			embed.add_field(name="Cog:", value=f'{cog}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
		except ExtensionNotLoaded:			
			
			embed = discord.Embed(color=embedcolor, title="Cog not found", description=f"Cog \"{cog}\" not found")
			embed.add_field(name="Cogs:", value=f'{cognames}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
		except ExtensionFailed as error:
			embed = discord.Embed(color=embedcolor, title="Cog errored")
			embed.add_field(name="Cog:", value=f'{cog}')
			embed.add_field(name="Error:", value=f'```{error}```', inline="false")
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
		print("cog: "+str(cog)+' reloaded by '+str(ctx.author))


def setup(bot):
    bot.add_cog(OwnerCog(bot))