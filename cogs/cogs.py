import os
import glob
import inspect
import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotLoaded, ExtensionFailed
from discord.ext.commands import Context
from customfunctions import config,master_logger,ErrorHandling

embedcolor = config("embedcolor")
logger = master_logger.getChild("cogs")

class CogDropdown(discord.ui.Select):
	def __init__(self, bot:discord.Client, cogs:"list[tuple[str,str]]"):
		self.bot = bot
		options = []
		for cog in cogs:
				options.append(discord.SelectOption(label=cog[1].split("/")[-1].replace("_", " ").title(), description=cog[1], value=cog[0]))

		
		super().__init__(placeholder='Choose cogs to load', min_values=1, max_values=len(options), options=options)
	
	async def callback(self, interaction:discord.Interaction):
		for cog in self.values:
			self.bot.load_extension(cog)
		await interaction.response.send_message(f'Loaded cogs', ephemeral=True)


class CogsCog(commands.Cog, name="Cogs"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx:Context, *cogs_to_reload):
		def format_cog_name(cog_name:str) -> str:
			return cog_name.replace('cogs.', '').replace('_', ' ').title().replace('.','/')

		cog_text_lines = []
		if len(cogs_to_reload) == 0:
			reload_cogs = [inspect.getmodule(cog).__name__ for cog in self.bot.cogs.values()]
		else:
			reload_cogs = [f'cogs.{cog.replace("cogs.", "").strip("./").replace(".py", "").replace("/", ".").replace(" ", "_").lower()}' for cog in cogs_to_reload]
		for cog in reload_cogs:
			try:
				self.bot.reload_extension(cog)
				cog_text_lines.append(f'<:Success:865674863330328626> | {format_cog_name(cog)}')
			except ExtensionFailed as error:
				cog_text_lines.append(f'<:Failure:865674863031877663> | {format_cog_name(cog)}')
				await ErrorHandling.uncaught_error(ctx, error,self.bot,silent=True)
		embed = discord.Embed(color=embedcolor, title="Reloading Cogs")
		cog_text_lines.sort()
		cog_text = "\n".join(cog_text_lines)
		embed.add_field(name="Cogs:", value=f'{cog_text}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
		await ctx.reply(embed=embed)


	@commands.command()
	@commands.is_owner()
	async def unload(self, ctx, cog):
		cog_lower = cog.lower()
		try:
			self.bot.unload_extension(cog)
			embed = discord.Embed(color=embedcolor, title="Unloaded Cog")
			embed.add_field(name="Cog:", value=f'{cog}')
			embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
			await ctx.reply(embed=embed)
		except ExtensionNotLoaded:
			try:
				self.bot.unload_extension(f'cogs.{cog_lower}')
				embed = discord.Embed(color=embedcolor, title="Unloaded Cog")
				embed.add_field(name="Cog:", value=f'{cog}')
				embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
				await ctx.reply(embed=embed)

			except:
				embed = discord.Embed(color=embedcolor, title="Cog Not Loaded")
				embed.add_field(name="Cog", value=cog)
				await ctx.reply(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def load(self, ctx, *, cog:str=None):
		if cog is not None:
			import_path:str = f'cogs.{cog.replace("cogs.", "").strip("./").replace(".py", "").replace("/", ".").replace(" ", "_").lower()}'
			file_path:str=f'{import_path.replace(".", "/")}.py'
			if os.path.exists(file_path):
				self.bot.load_extension(import_path)
				await ctx.send("Cog sucessfully loaded")
			else:
				await ctx.reply(f"Cannot find cog at {file_path}")
		else:
			cogs = [(file.replace(".py", "").replace("/", "."), file.replace(".py", "").replace("cogs/", "")) for file in glob.glob("cogs" + '/**/*.py', recursive=True) if not file.endswith("__.py")]
			cogs = [cog for cog in cogs if not cog[0] in [inspect.getmodule(cog).__name__ for cog in self.bot.cogs.values()]]
			if len(cogs) > 0:
				bot = self.bot
				class CogsDropdownView(discord.ui.View):
					def __init__(self):
						super().__init__()

						# Adds the dropdown to our view object.
						self.add_item(CogDropdown(bot, cogs))

				await ctx.send("Select cogs to load", view=CogsDropdownView())
			else:
				await ctx.send("All cogs are already loaded")

def setup(bot):
	bot.add_cog(CogsCog(bot))
