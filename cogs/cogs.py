import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotLoaded, ExtensionNotFound, ExtensionFailed
from customfunctions import config


embedcolor = int(config("embedcolor"), 16)




class CogsCog(commands.Cog, name="Cogs"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, cog_to_reload="all"):
		cognames = [cog.capitalize() for cog in [ cog.replace('cogs.', '').replace('-', ' ') for cog in ctx.bot.coglist]]
		cognames = '\n'.join(cognames)
		ccog_to_reloadog = cog_to_reload.lower()
		if cog_to_reload=="all":
			for cog in ctx.bot.coglist:
				self.bot.reload_extension(cog)
			embed = discord.Embed(color=embedcolor, title="Reloading Cogs...")
			embed.add_field(name="Cogs:", value=f'{cognames}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
		else:
			try:
				self.bot.reload_extension(f'cogs.{cog_to_reload}')
				embed = discord.Embed(color=embedcolor, title="Reloading Cog...")
				embed.add_field(name="Cog:", value=f'{cog_to_reload}')
				embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
				await ctx.reply(embed=embed)
			except ExtensionNotLoaded:
				try:
					self.bot.load_extension(f'cogs.{cog_to_reload}')
					embed = discord.Embed(color=embedcolor, title="Cog Loaded")
					embed.add_field(name="Cog", value=cog_to_reload)
					ctx.reply(embed=embed)
				except ExtensionNotFound:
					embed = discord.Embed(color=embedcolor, title="Cog not found", description=f"Cog \"{cog_to_reload}\" not found")
					embed.add_field(name="Cogs:", value=f'{cognames}')
					embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
					await ctx.reply(embed=embed)
			except ExtensionFailed as error:
				embed = discord.Embed(color=embedcolor, title="Cog errored")
				embed.add_field(name="Cog:", value=f'{cog_to_reload}')
				embed.add_field(name="Error:", value=f'```{error}```', inline="false")
				embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
				await ctx.reply(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, cog):
		cog_lower = cog.lower()
		try:
			self.bot.unload_extension(cog)
			embed = discord.Embed(color=embedcolor, title="Unloaded Cog")
			embed.add_field(name="Cog:", value=f'{cog}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
		except ExtensionNotLoaded as error:
			try:
				self.bot.unload_extension(f'cogs.{cog_lower}')
				embed = discord.Embed(color=embedcolor, title="Unloaded Cog")
				embed.add_field(name="Cog:", value=f'{cog}')
				embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
				await ctx.reply(embed=embed)

			except:
				embed = discord.Embed(color=embedcolor, title="Cog Not Loaded")
				embed.add_field(name="Cog", value=cog)
				await ctx.reply(embed=embed)



def setup(bot):
	bot.add_cog(CogsCog(bot))
