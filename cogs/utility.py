import time
import datetime
import asyncio
import json
from types import CoroutineType, coroutine
from typing import Coroutine
import discord
import inspect
from discord.ext import commands
from discord.ext.commands.converter import Greedy


from disputils import BotEmbedPaginator
from customfunctions import EmbedMaker, CustomChecks
from customfunctions import config
from customfunctions import TimeUtils
from customfunctions import master_logger

logger = master_logger.getChild("utility")
embedcolor = config("embedcolor")





class UtilityCog(commands.Cog, name="Utility"):
	def __init__(self, bot):
		self.bot:discord.Client = bot

	@commands.command()
	async def help(self, ctx, *, command_name:str=None):
		"""**Shows information about commands. You can optionally specify a command to see more information**
		
		*Parameters*
		
		> `command_name` should be the fully qualified name of a command, and you can use aliases. `%help minecraft server` and `%help mc server` will both give you the help page for `%minecraft server`. If it is not included, it will show a list of commands paginated by cog

		*Information*

		> `Cog` shows what cog a command is in. This is only really useful for the owner.
		> `Usage` shows the position of arguments. Arguments surrounded by <angled brackets> are required, and arguments surrounded by [square brackets] are optional
		> `Enabled` shows whether the command is enabled. If it is disabled, nobody can use it.
		> `Can Execute` shows whether the commmand can be run with the current context. This will be false if you don't have permissions, you're in the wrong server, etc
		"""
		pages   = []
		if command_name is None:
			for cog, cog_data in self.bot.cogs.items():
				cog:str
				cog_data:commands.Command
				cog_commands:"list[commands.Command|commands.Group]" = []
				logger.debug(f"Starting cog loop for {cog}")

				for command in cog_data.walk_commands():
					command:"commands.Command|commands.Group"
					if command.hidden or not command.enabled:
						pass
					else:
						short_help = " - "+command.help.split("\n")[0] if command.help is not None else ""
						signature = f" {command.signature}" if command.signature != "" else ""
						cog_commands.append(f'''`{self.bot.prefix}{command.qualified_name}{signature}` {short_help}''')

				cog_help_page="\n".join(cog_commands)

				if hasattr(cog_data, "hide_help") and cog_data.hide_help:
					if ctx.author.id == self.bot.owner.id:
						pages.append(discord.Embed(title=f'Help: {cog}', description=cog_help_page, color=embedcolor))

				elif hasattr(cog_data, "guild_limit"):
					if CustomChecks.check_enabled_guild(ctx, cog_data.guild_limit):
						pages.append(discord.Embed(title=f'Help: {cog}', description=cog_help_page, color=embedcolor))

				else:
					pages.append(discord.Embed(title=f'Help: {cog}', description=cog_help_page, color=embedcolor))

			paginator = BotEmbedPaginator(ctx, pages)
			await paginator.run()
		else:
			bot_commands:"list[commands.Command|commands.Group]" = self.bot.walk_commands()
			split_command_name = command_name.split(" ")
			command = None
			for bot_command in bot_commands:
				if len(split_command_name) == 1:
					if split_command_name[0] in bot_command.aliases or split_command_name[0] == bot_command.name:
						command = bot_command
						break
				if len(bot_command.parents) == len(split_command_name[:-1]):
					matching_parents=[]
					for index, parent in enumerate(split_command_name[:-1]):
						matching_parents.append(parent in bot_command.parents[index].aliases or parent == bot_command.parents[index].name)
					if all(matching_parents):
						if split_command_name[-1] == bot_command.name or split_command_name[-1] in bot_command.aliases :
							command = bot_command
							break
			if command is None:
				await ctx.reply(f"Command '{command_name}' not found")
			else:
				embed = discord.Embed(color=embedcolor,title=f'{self.bot.prefix}{command_name.lower()}', description="\n\n".join([item for item in (command.description, command.help) if item is not None]))
				embed.set_author(name="SachiBot Help")
				embed.add_field(name="Cog", value=command.cog_name)
				signature = f" {command.signature}" if command.signature != "" else ""
				embed.add_field(name="Usage", value=f'`{self.bot.prefix}{command.qualified_name}{signature}`')
				embed.add_field(name="Enabled", value=command.enabled)
				if isinstance(command, commands.Group):
					subcommands = "\n".join([f'`{self.bot.prefix}{subcommand.qualified_name}`' for subcommand in command.commands])
					embed.add_field(name="Subcommands",value=subcommands)
				check_results = []
				for check in command.checks:
					try:
						check_results.append(await check(ctx))
					except Exception:
						check_results.append(False)
				cog:commands.Cog = command.cog
				try:
					if inspect.iscoroutinefunction(cog.cog_check):
						check_results.append(await cog.cog_check(ctx))
					else:
						check_results.append(cog.cog_check(ctx))
				except:
					check_results.append(False)
				logger.info(check_results)
				embed.add_field(name="Can Execute", value=all(check_results))
				await ctx.reply(embed=embed)

	@commands.command(aliases=['uptime'])
	async def ping(self, ctx):
		current_time = time.time()
		difference   = int(round(current_time - ctx.bot.start_time))
		uptime       = str(datetime.timedelta(seconds=difference))
		embed        = discord.Embed(color=embedcolor)
		embed.add_field(name="Ping", value=f'🏓 Pong! {round(self.bot.latency * 1000)}ms', inline='false')
		embed.add_field(name="Uptime", value=f'{uptime}')
		embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
		await ctx.reply(embed=embed)


	# @commands.command(aliases=['userinfo'])
	# async def whois(self,ctx, members:Greedy[discord.Member]=None, users:Greedy[discord.User]=None):
	# 	for member in members:

	# 	statuseemojis  = {
	# 			"online" : "🟢",
	# 			"idle"   : "🟡",
	# 			"dnd"    : "🔴",
	# 			"offline": "⚫"

	# 		}
	# 	if isguildmember:
	# 		if member.is_on_mobile():
	# 			platform  = '📱 - '
	# 		elif str(user.status) != "offline":
	# 			platform = '💻 - '
	# 		else:
	# 			platform = ""
	# 	else:
	# 		assert user is discord.User
	# 		platform = None
	# 	flags = user.public_flags.all()
	# 	badgelist = {
	# 		"staff"                 : "<:developer:802021494778626080>",
	# 		"partner"               : "<:partneredserverowner:802021495089004544>",
	# 		"hypesquad"             : "<:hypesquad:802021494925557791>",
	# 		"bug_hunter"            : "<:bughunterl1:802021561967575040>",
	# 		"hypesquad_bravery"     : "<:hypesquadbravery:802021495185473556>",
	# 		"hypesquad_brilliance"  : "<:hypesquadbrilliance:802021495433461810>",
	# 		"hypesquad_balance"     : "<:hypesquadbalance:802010940698132490>",
	# 		"early_supporter"       : "<:earlysupporter:802021494989389885>",
	# 		"bug_hunter_level_2"    : "<:bughunterl2:802021494975889458>",
	# 		"verified_bot_developer": "<:earlybotdeveloper:802021494875488297>"
	# 	}
	# 	flagnames = [flag.name for flag in flags]
	# 	badgeicons = [badgelist[badge] for badge in badgelist if badge in flagnames]
	# 	badgestr   = " ".join(list(map(str, badgeicons)))

	# 	avatar     = user.avatar.url
	# 	mention    = user.mention
	# 	username   = user.name+"#"+user.discriminator
	# 	color      = user.color

	# 	embed       = discord.Embed(color=color,title=username)
	# 	embed.set_footer(text=f"Request by {ctx.author}", icon_url= ctx.author.avatar.url)
	# 	embed.set_image(url=avatar)
	# 	if isguildmember:
	# 		EmbedMaker.add_description_field(embed, "Is a bot?", user.bot)
	# 		EmbedMaker.add_description_field(embed, "Is the owner?", bool(ctx.guild.owner.id == user.id))
	# 		EmbedMaker.add_description_field(embed, "Is an admin?", user.guild_permissions.administrator)
	# 		EmbedMaker.add_blank_field(embed)
	# 		EmbedMaker.add_description_field(embed, "Status", f"{platform}{statuseemojis[str(user.status)]}{f' | {user.activity.name}' if user.activity is not None else ''}")
	# 		EmbedMaker.add_blank_field(embed)
	# 	EmbedMaker.add_description_field(embed, "Mention", mention)
	# 	if isguildmember:
	# 		EmbedMaker.add_description_field(embed, "Nickname", user.display_name)
	# 	EmbedMaker.add_description_field(embed, "User ID", f'`{user.id}`')
	# 	EmbedMaker.add_blank_field(embed)
	# 	EmbedMaker.add_description_field(embed, "Account Creation Date", user.created_at)
	# 	if isguildmember:
	# 		EmbedMaker.add_description_field(embed, "Join Date", user.joined_at)
	# 	EmbedMaker.add_blank_field(embed)
	# 	if str(badgeicons) != "[]":
	# 		EmbedMaker.add_description_field(embed, "Profile Badges", badgestr)

	# 	await ctx.send(embed=embed)
	# 	#ctx.guild.get_member(user)

	@commands.command()
	async def suggest(self, ctx, *, suggestion):
		suggestion_channel = self.bot.get_channel(801576966952058910)
		embed = discord.Embed(title='', description=suggestion)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
		await suggestion_channel.send(embed=embed)
		await ctx.reply("Suggestion added")


	@commands.command()
	@commands.is_owner()
	async def selfmute(self, ctx, duration_str: str, *, sleep:bool=False):
		try:
			duration = TimeUtils.parse(duration_str)
		except ValueError:
			await ctx.reply("Please write your duration in the format of '10m'")
			return
		muted_role = discord.utils.get(ctx.guild.roles, name='Muted') # fetch role with name 'muted'
		unmute_timestamp = TimeUtils.get_future_time(duration).timestamp() # Get a timestamp for the duration specified
		with open("storage/mutes.json", "w") as file:
			muted_list = self.bot.mutes
			muted_list.append({"userid":ctx.author.id, "expiration": unmute_timestamp, "guild": ctx.guild.id, "msg_id": ctx.message.id, "role": muted_role.id}) # add new mute
			json.dump(muted_list, file, indent=2) # dump new data

		await ctx.author.add_roles(muted_role, reason=f"Requested self-mute for {duration_str}")

		await ctx.reply(f"Muting for {duration_str} ...")

		#sleep for the duration
		if sleep:
			await asyncio.sleep(duration)
			# Remove mute from storage
			with open("storage/mutes.json", "w") as file:
				muted_list:list = self.bot.mutes
				index = [i for i,dct in enumerate(muted_list) if dct["userid"] == ctx.author.id and dct["msg_id"] == ctx.message.id][0]
				muted_list.pop(index)
				json.dump(muted_list, file, indent=2)

			await ctx.author.remove_roles(muted_role, reason=f"Requested self-mute for {duration_str} has expired")
			await ctx.send(f"{ctx.author.mention}, your self mute for {duration_str} seconds has expired")


	@commands.command(aliases=["online", "areyouthere"])
	async def didyoudie(self, ctx):
		await ctx.reply("I am very much alive", delete_after=20)

	@commands.command(aliases=["vote"])
	async def react(self, ctx, message:discord.Message, *args):
		"""Reacts to a message with a set of emojis
		Valid sets are "existing", "yesno", "updown", "checkx", and "shrug"
		"""
		if not (message.channel.permissions_for(ctx.author).manage_messages or ctx.author.id == self.bot.owner.id):
			await ctx.reply("You need manage messages to do that")
			return
		emojis:"list[discord.Emoji]" = []
		reactions = {
			"existing": message.reactions,
			"yesno": ["<:yes:836795924977549362>", "<:no:836795924633354332>"],
			"updown": ["<:upvote:771082566752665681>", "<:downvote:771082566651609089>"],
			"checkx": ["<:yes:786997173845622824>","<:no:786997173820588073>"],
			"shrug": ["🤷"],
			"_unicode": ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
		}
		emoji_sets:"list[str]" = [set_name for set_name in args if (set_name in reactions.keys() and set_name != "_unicode")]
		for emoji_name in args:
			if not (emoji_name.isdigit() or emoji_name in reactions.keys()):
				try:
					emoji = await commands.EmojiConverter().convert(ctx,emoji_name)
					emojis.append(emoji)
				except commands.EmojiNotFound:
					pass
		logger.debug(emojis)
		for count in [arg for arg in args if arg.isdigit()]:
			emojis = emojis+[reactions["_unicode"][num] for num in range(0, int(count)) if num < 10]
		for emoji_set in emoji_sets:
			emojis = emojis + reactions[emoji_set]
		for emoji in emojis:
			if emoji is not None:
				await message.add_reaction(emoji)
		await ctx.message.add_reaction("👍")

def setup(bot):
	bot.add_cog(UtilityCog(bot))
