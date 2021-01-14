import discord
from discord.ext import commands
import json
import time, datetime
import os, sys

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

	@commands.command(aliases=['reload'])
	async def restart(self, ctx):
		if ctx.message.author.id != 545463550802395146:
				await ctx.message.add_reaction(str('🔒'))
				return
		else:
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
	async def stop(self, ctx):
		if ctx.message.author.id != 545463550802395146:
			await ctx.message.add_reaction(str('🔒'))
			return
		else:
			await ctx.message.delete()
			embed = discord.Embed(color=embedcolor, title="Stopping...")
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.send(embed=embed)
			print('Bot stopped by '+str(ctx.author))
			await os.system("pm2 stop 0")
			await self.bot.logout()

	@commands.command()
	async def export(self, ctx, channel):
		if ctx.message.author.id != 545463550802395146:
			await ctx.message.add_reaction(str('🔒'))
			return
		else:
			embed = discord.Embed(color=embedcolor)
			embed.add_field(name="Channel", value=f'{channel}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
			print('Exported by '+str(ctx.author))




def setup(bot):
    bot.add_cog(OwnerCog(bot))