import discord
from discord.ext import commands
from customfunctions import config, MinecraftApi


embedcolor = config("embedcolor")

class MinecraftCog(commands.Cog, name="Minecraft"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@commands.group(aliases=["mc"])
	async def minecraft(self, ctx):
		if ctx.invoked_subcommand is None:
			subcommands = [
				f'**`{cmd.name}`:** {cmd.help}' for cmd in ctx.command.commands]
			embed = discord.Embed(color=embedcolor, title="Minecraft Subcommands:",
								  description="\n\n".join(list(map(str, subcommands))))
			await ctx.reply(embed=embed)

	@minecraft.command()
	async def skin(self, ctx, username:str):
		"""
		Shows a 3D render of a user's skin
		"""
		try:
			user = MinecraftApi.MinecraftUser(username)
		except ValueError:
			await ctx.reply("Invalid username")
		embed = discord.Embed(title=user.name,color=embedcolor)
		embed.set_footer(text="Avatars provided by Crafatar.com")
		embed.set_image(url=user.skin("body_render"))
		await ctx.reply(embed=embed)

	@minecraft.command()
	async def uuid(self, ctx, username:str):
		"""
		Gets the user's uuid from their username
		"""
		try:
			user = MinecraftApi.MinecraftUser(username)
		except ValueError:
			await ctx.reply("Invalid username")
		await ctx.reply(f'`{user.uuid}`')

def setup(bot):
	bot.add_cog(MinecraftCog(bot))
