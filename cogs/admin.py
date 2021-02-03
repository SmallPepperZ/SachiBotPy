import discord
from discord.ext import commands
import json
from discord.ext.commands import MessageConverter
import logging

#region Variable Stuff

with open('storage/config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
prefix = configjson["prefix"]
#endregion



class AdminCog(commands.Cog, name="Admin"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def purge(self, ctx):
		if ctx.message.author.id != 545463550802395146:
			await ctx.message.add_reaction(str('🔒'))
			return
		else:
			args = ctx.message.content.split(" ")
			if args[1]:
				try:
					amount = int(args[1])
					await ctx.message.delete()				
					await ctx.channel.purge(limit=amount)
					embed = discord.Embed(color=embedcolor)
					embed.add_field(name="Clear", value="cleared " + args[1] + " messages")
					embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
					await ctx.send(embed=embed)
				except:
					await ctx.reply("Error, most likely not a number")

	@commands.command()
	async def delete(self, ctx, messageid):
		if ctx.message.author.id != 545463550802395146:
			await ctx.message.add_reaction(str('❔'))
			return
		else:
			await ctx.message.delete()
			message = await MessageConverter().convert(ctx, messageid)
			await message.delete()




def setup(bot):
    bot.add_cog(AdminCog(bot))