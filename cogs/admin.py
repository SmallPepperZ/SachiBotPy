import discord
from discord.ext import commands
from discord.ext.commands import MessageConverter
from customfunctions import config

#region Variable Stuff


embedcolor = int(config("embedcolor"), 16)
#endregion



class AdminCog(commands.Cog, name="Admin"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_guild_permissions(manage_messages=True)
	async def purge(self, ctx):
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
	@commands.has_guild_permissions(manage_messages=True)
	async def delete(self, ctx, messageid):
		message:discord.Message = await MessageConverter().convert(ctx, messageid)
		if message.guild.id == ctx.guild.id:	
			await ctx.message.delete()
			await message.delete()


	@commands.command()
	@commands.has_guild_permissions(manage_nicknames=True)
	async def nickname(self, ctx:commands.Context, *args):
		args = list(args)
		if len(ctx.message.mentions) == 1:
			user = ctx.message.mentions[0]
			args.pop(args.index(user.mention))
		else:
			user = await ctx.guild.fetch_member(args[0])
			args.pop(args.index(user.id))
		nick = ' '.join(args)
		await user.edit(nick=nick)


def setup(bot):
    bot.add_cog(AdminCog(bot))