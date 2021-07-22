import discord
from discord.ext import commands
from customfunctions import config, MinecraftApi, master_logger, EmbedMaker


embedcolor = config("embedcolor")
logger = master_logger.getChild("minecraft")

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
		"""Shows a 3D render of a user's skin"""
		try:
			user = MinecraftApi.MinecraftUser(username)
		except ValueError:
			await ctx.reply("Invalid username")
			return
		embed = discord.Embed(title=user.name,color=embedcolor)
		embed.set_footer(text="Avatars provided by Crafatar.com")
		embed.set_image(url=user.skin("body_render"))
		await ctx.reply(embed=embed)

	@minecraft.command(aliases=["id", "userid"])
	async def uuid(self, ctx, username:str):
		"""Gets the user's uuid from their username"""
		try:
			user = MinecraftApi.MinecraftUser(username)
		except ValueError:
			await ctx.reply("Invalid username")
			return
		await ctx.reply(f'`{user.uuid}`')

	@minecraft.command()
	async def name_history(self, ctx, user:str):
		"""Gets a user's name history from their uuid or username"""
		try:
			user_data = MinecraftApi.MinecraftUser(user)
		except ValueError:
			await ctx.reply("Invalid username/UUID")
			return
		embed = discord.Embed(title="Name History", color=embedcolor)
		embed.set_author(name=user_data.name, icon_url=user_data.get_skin())
		names = []
		for name_entry in user_data.name_history:
			if "changedToAt" in name_entry.keys():
				names.append(f'<t:{int(name_entry["changedToAt"]/1000)}> | {name_entry["name"]}')
			else:
				names.append(name_entry["name"])
		names.reverse()
		embed.__setattr__("description", "\n".join(names))
		await ctx.send(embed=embed)

	@minecraft.command()
	async def server(self, ctx, server_ip:str, port:int=25565):
		"""Gets information about a Minecraft Server"""
		server = MinecraftApi.MinecraftServer(server_ip, port)
		embed = discord.Embed(color=server.color, title="Server Status")
		embed.set_author(name=server.ip)
		embed.set_thumbnail(url=server.server_icon)
		status = "Online" if server.online else "Offline"
		EmbedMaker.add_description_field(embed, "Status", status)
		if server.online:
			EmbedMaker.add_description_field(embed, "Version", server.version)
			EmbedMaker.add_description_field(embed, "Software", server.software)
			EmbedMaker.add_description_field(embed, "Player Count", f'{server.players.count}/{server.players.max}')
			formatted_motd = "\n".join([f"> {line}" for line in server.motd])
			EmbedMaker.add_description_field(embed, None, f'\n{formatted_motd}')
			if server.mods is not None:
				EmbedMaker.add_description_field(embed, "Mods", ", ".join(server.mods))
			if server.plugins is not None:
				EmbedMaker.add_description_field(embed, "Plugins", ", ".join(server.plugins))
			if server.players.names is not None:
				EmbedMaker.add_description_field(embed, "Players", ", ".join(server.players.names))
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(MinecraftCog(bot))
