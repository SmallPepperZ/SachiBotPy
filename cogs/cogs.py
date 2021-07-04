import discord
from discord.ext import commands
from discord.ext.commands.errors import ExtensionNotLoaded, ExtensionFailed
from discord.ext.commands import Context
from customfunctions import config,master_logger,ErrorHandling

embedcolor = config("embedcolor")
logger = master_logger.getChild("cogs")



class CogsCog(commands.Cog, name="Cogs"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@commands.command()
	@commands.is_owner()
	async def reload(self, ctx:Context, *cogs_to_reload):
		def format_cog_name(cog_name:str) -> str:
			return cog_name.replace('cogs.', '').replace('_', ' ').title()
		cog_text_lines = []
		if len(cogs_to_reload) == 0:
			reload_cogs = self.bot.coglist
		else:
			reload_cogs = [f'cogs.{cog.lower()}' for cog in cogs_to_reload]
		for cog in reload_cogs:
			try:
				self.bot.reload_extension(cog)
				cog_text_lines.append(f'<:yes:786997173845622824> | {format_cog_name(cog)}')
			except ExtensionFailed as error:
				cog_text_lines.append(f'<:no:786997173820588073> | {format_cog_name(cog)}')
				await ErrorHandling.uncaught_error(ctx, error,self.bot,silent=True)
		embed = discord.Embed(color=embedcolor, title="Reloading Cogs")
		cog_text = "\n".join(cog_text_lines)
		embed.add_field(name="Cogs:", value=f'{cog_text}')
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
