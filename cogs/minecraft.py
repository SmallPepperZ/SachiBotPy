import discord
from discord.ext import commands
from customfunctions import config, MinecraftApi, master_logger, EmbedMaker, DBManager


embedcolor = config("embedcolor")
logger = master_logger.getChild("minecraft")
database = DBManager.Database()

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
		# embed.set_footer(text="Avatars provided by Crafatar.com")
		embed.set_image(url=user.get_skin("head_render"))
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

	@minecraft.command(aliases=["status", "serverstatus"])
	async def server(self, ctx, server:str="default", port:int=25565, save_name:str=None):
		"""Gets information about a Minecraft Server

		> `server` should be the numeric ip address for the server, eg 123.456.789.012. It can also be a server's saved name, if it is saved. 
		> `port` should be the port of the server, 25565 by default
		> `save_name` is used to save the server so it can be easily accessed again. If the server name is "default", it will be used when no guild is specified. Saving a server as default requires manage messages
		"""
		database.cursor.execute("""CREATE TABLE IF NOT EXISTS mc_servers (
			guild_id     INT  NOT NULL,
			owner_id     INT              NOT NULL,
			ip_address   TEXT             NOT NULL,
			port         INT              NOT NULL,
			name         TEXT             NOT NULL,
			PRIMARY KEY (guild_id,name))""")
		stored_server = database.cursor.execute("SELECT * FROM mc_servers WHERE guild_id=? AND name=?", (ctx.guild.id,server)).fetchone()
		database.commit()
		if stored_server is not None:
			server_ip = stored_server[2]
			server_port = stored_server[3]
		else:
			server_ip = server
			server_port = port
		author:discord.Member = ctx.author
		if save_name is not None:
			if database.cursor.execute("SELECT * FROM mc_servers WHERE guild_id=? AND name=?", (ctx.guild.id,save_name)).fetchone() is None and save_name != "default":
				database.cursor.execute("INSERT INTO mc_servers (guild_id, owner_id, ip_address, port, name) values (?,?,?,?,?)", (ctx.guild.id, ctx.author.id, server, port, save_name))
				database.commit()
			elif author.guild_permissions.manage_messages:
				database.cursor.execute("INSERT OR REPLACE INTO mc_servers (guild_id, owner_id, ip_address, port, name) values (?,?,?,?,?)", (ctx.guild.id, ctx.author.id, server, port, save_name))
				database.commit()
				server_ip = server
				server_port = port
			else:
				database.commit()
		await ctx.channel.trigger_typing()
		server_data = MinecraftApi.MinecraftServer(server_ip, server_port)
		embed = discord.Embed(color=server_data.color, title="Server Status")
		embed.set_author(name=server_data.ip)
		embed.set_thumbnail(url=server_data.server_icon)
		status = "Online" if server_data.online else "Offline"
		EmbedMaker.add_description_field(embed, "Status", status)
		if server_data.online:
			EmbedMaker.add_description_field(embed, "Version", server_data.version)
			EmbedMaker.add_description_field(embed, "Software", server_data.software)
			EmbedMaker.add_description_field(embed, "Player Count", f'{server_data.players.count}/{server_data.players.max}')
			formatted_motd = "\n".join([f"> {line}" for line in server_data.motd])
			EmbedMaker.add_description_field(embed, None, f'\n{formatted_motd}')
			if server_data.mods is not None:
				EmbedMaker.add_description_field(embed, "Mods", ", ".join(server_data.mods))
			if server_data.plugins is not None:
				EmbedMaker.add_description_field(embed, "Plugins", ", ".join(server_data.plugins))
			if server_data.players.names is not None:
				EmbedMaker.add_description_field(embed, "Players", ", ".join(server_data.players.names))
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(MinecraftCog(bot))
