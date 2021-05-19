# region Imports

import time
import json
import logging
import traceback
import discord

import requests

from discord.enums import Status
from discord.ext import commands
from discord.ext.commands import CommandNotFound, errors
from discord_slash import SlashCommand


from customfunctions import config, set_config
from customfunctions import CustomChecks
# endregion

# region Variable Stuff


embedcolor = int(config("embedcolor"), 16)
token = config('discordtoken')

personal_info = config("pathtohide")


prefix = config("prefix")
start_time_local = time.time()

intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(command_prefix=prefix,
				   intents=intents,
				   case_insensitive=True)

slash = SlashCommand(bot, override_type=True, sync_commands=True)

errorchannel = int(config("errorchannel"))

bot.start_time = start_time_local
logging.basicConfig(level=logging.INFO)


bot.remove_command('help')

bot.enabled_guilds = [764981968579461130, #MDSP
					  813992520915615796, #Gapple
					  797308956162392094, #SachiBotLand
					  739176312081743934  #Notifications
					  ]
# endregion


# region Cogs
bot.coglist = [	'cogs.owner',
				'cogs.fun',
				'cogs.utility',
				'cogs.admin',
				'cogs.cogs',
				'cogs.listeners',
				'cogs.testing',
				'cogs.mdsp',
				'cogs.slash-commands'
				]

if __name__ == '__main__':
	for extension in bot.coglist:
		bot.load_extension(extension)
# endregion

# region Logger Stuff
logger = logging.getLogger("Discord - Main")
logger.setLevel(logging.INFO)


# endregion

@bot.event
async def on_ready():
	logger.info("Bot initialized")
	status = config('status')
	await bot.change_presence(activity=discord.Activity(type=status[0][1], name=status[1]), status=status[2][1])


# region Bot Events

@bot.event
async def on_command_error(ctx, error):
	if hasattr(ctx.command, 'on_error'):
		return
	elif isinstance(error, CommandNotFound) or ctx.command.hidden:
		await ctx.message.add_reaction(str('❔'))
		return
	elif isinstance(error, errors.NotOwner):
		await ctx.message.add_reaction(str('🔏'))
		return
	elif isinstance(error, errors.DisabledCommand):
		await ctx.message.add_reaction(str('<:DisabledCommand:804476191268536320>'))
		return
	elif isinstance(error, errors.MissingPermissions):
		await ctx.message.add_reaction(str('🔐'))
		return
	elif isinstance(error, errors.BotMissingPermissions):
		await ctx.reply("I do not have the requisite permissions")
		return
	elif isinstance(error, errors.MissingRole):
		await ctx.message.add_reaction(str('🔐'))
		return
	elif isinstance(error, errors.CommandOnCooldown):
		await ctx.message.add_reaction(str('<:Cooldown:804477347780493313>'))
		if str(error.cooldown.type.name) != "default":
			cooldowntype = f'per {error.cooldown.type.name}'
		else:
			cooldowntype = 'global'
			await ctx.reply(f"This command is on a {round(error.cooldown.per, 0)}s {cooldowntype} cooldown. "
							f"Wait {round(error.retry_after, 1)} seconds",
							delete_after=min(10, error.retry_after))
		return
	elif isinstance(error, errors.MissingRequiredArgument):
		await ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`", delete_after=30)
		return
	elif isinstance(error, errors.BadArgument):
		await ctx.reply(f"Invalid argument!\nUsage: `{ctx.command.signature}`", delete_after=30)
		return
	elif isinstance(error, errors.NoPrivateMessage):
		await ctx.message.add_reaction(str('<:ServerOnlyCommand:803789780793950268>'))
		return
	elif isinstance(error, CustomChecks.IncorrectGuild):
		await ctx.reply(content="This command does not work in this server.", delete_after=10)
		return
	else:
		# Send user a message

		error_str = str(error).replace(personal_info, '')
		await ctx.message.add_reaction('<:CommandError:804193351758381086>')
		await ctx.reply("Error:\n```"+error_str+"```\nSmallPepperZ will be informed", delete_after=60)

		# Get traceback info
		
		exc = error
		error_type = type(exc)
		trace = exc.__traceback__

		lines = traceback.format_exception(error_type, exc, trace)
		traceback_text = ''.join(lines)

		# Github gist configuration
		errornum = config("errornum")
		errornum = int(errornum)+1
		set_config("errornum", str(errornum))

		traceback_text = traceback_text.replace(personal_info, '')

		apiurl = "https://api.github.com/gists"
		gist_id = config("githubgist")
		gisttoedit = f'{apiurl}/{gist_id}'
		githubtoken = config('githubtoken')

		headers = {'Authorization': 'token %s' % githubtoken}
		params = {'scope': 'gist'}
		content = f'Error - {error} \n\n\n {traceback_text}'
		formatted_error_number = f'{errornum:02d}'
		payload = {"description": "SachiBot Errors - A gist full of errors for my bot", "public": False,
				   "files": {"SachiBotPyError %s.log" % formatted_error_number: {"content": content}}}
		# Upload to github gist
		requests.patch(gisttoedit,
					   headers=headers,
					   params=params,
					   data=json.dumps(payload))
		# Build and send embed for error channel
		channel = bot.get_channel(errorchannel)
		embed1 = discord.Embed(
			title=f"Error {formatted_error_number}", color=embedcolor)
		embed1.add_field(name="Message Url:",
						 value=ctx.message.jump_url, inline='false')
		embed1.add_field(
			name="Message:", value=ctx.message.clean_content, inline='true')
		embed1.add_field(
			name="Author:", value=ctx.message.author.mention, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		# Check if it was in a guild
		try:
			guildname = ctx.guild.name
			channelname = ctx.channel.name
		except:
			guildname = "DM"
			channelname = ctx.author.id
		embed1.add_field(name="Guild:", value=guildname, inline='true')
		embed1.add_field(name="Channel:", value=channelname, inline='true')
		embed1.add_field(name="\u200B", value='\u200B', inline='true')
		embed1.add_field(name="Error:", value=f'```{error}```', inline='false')
		embed1.add_field(
			name="Traceback:", value=f'Traceback Gist - '
									 f'[SachiBotPyError {formatted_error_number}.log](https://gist.github.com/SmallPepperZ/{gist_id}#file-sachibotpyerror-{formatted_error_number}-log'
									 f' \"Github Gist #{formatted_error_number}\") ', inline='false')
		await channel.send(embed=embed1)

		ghost_ping = await channel.send('<@!545463550802395146>')
		await ghost_ping.delete()


@bot.event
async def on_member_join(member: discord.Member):
	member_join_update(member, "joined")

@bot.event
async def on_member_remove(member: discord.Member):
	member_join_update(member, "left")

async def member_join_update(member:discord.Member, action:str) -> None:
	channel:discord.TextChannel = bot.get_guild(797308956162392094).get_channel(844600626516328519)
	embed = discord.Embed(title=f'User {action.capitalize()}', description=f"""
	**Guild**
	ID  : `{member.guild.id}`
	Name: {member.guild.name}
	**User**
	ID     : `{member.id}`
	Name   : {member.name}
	Mention: {member.mention}
	""")
	await channel.send(embed=embed)
# endregion


bot.run(token)
