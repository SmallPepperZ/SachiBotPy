import discord
from discord.ext import commands
import json
from discord.ext.commands.errors import ExtensionNotLoaded
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import ExtensionFailed

#region Variable Stuff

with open('config.json', 'r') as file:
	configfile = file.read()

configjson = json.loads(configfile)
embedcolor = int(configjson["embedcolor"], 16)
token = configjson["token"]
prefix = configjson["prefix"]
#endregion



class CogsCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx, cog):
		cogs = str(ctx.bot.coglist)
		cog = cog.lower()
		cognames = cogs.replace('cogs.', '').replace('[', '').replace(']', '').replace("\'", "").replace(",", "\n")
		try:
			self.bot.reload_extension(f'cogs.{cog}')
			embed = discord.Embed(color=embedcolor, title="Reloading Cog...")
			embed.add_field(name="Cog:", value=f'{cog}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
		except ExtensionNotLoaded:
			try:
				self.bot.load_extension(f'cogs.{cog}')
				embed = discord.Embed(color=embedcolor, title="Cog Loaded")
				embed.add_field(name="Cog", value=cog)
				ctx.reply(embed=embed)
			except ExtensionNotFound:
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
		print(f'{ctx.message.author.name} ({ctx.message.author.id}) just used \'{prefix}reload {cog}\'')

	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, cog):
		cogs = str(ctx.bot.coglist)
		cog_lower = cog.lower()
		cognames = cogs.replace('cogs.', '').replace('[', '').replace(']', '').replace("\'", "").replace(",", "\n")
		try:
			self.bot.unload_extension(cog)
			embed = discord.Embed(color=embedcolor, title="Unloaded Cog")
			embed.add_field(name="Cog:", value=f'{cog}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
			await ctx.reply(embed=embed)
			print(f'{ctx.message.author.name} ({ctx.message.author.id}) just used \'{prefix}unload {cog}\'')
		except ExtensionNotLoaded as error:
			try:
				self.bot.unload_extension(f'cogs.{cog_lower}')
				embed = discord.Embed(color=embedcolor, title="Unloaded Cog")
				embed.add_field(name="Cog:", value=f'{cog}')
				embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar_url)
				await ctx.reply(embed=embed)
				print(f'{ctx.message.author.name} ({ctx.message.author.id}) got handled error "ExtensionNotLoaded" when using \'{prefix}unload {cog}\'')
			except:
				embed = discord.Embed(color=embedcolor, title="Cog Not Loaded")
				embed.add_field(name="Cog", value=cog)
				await ctx.reply(embed=embed)
		
			

def setup(bot):
	bot.add_cog(CogsCog(bot))