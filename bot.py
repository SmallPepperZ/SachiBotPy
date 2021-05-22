# region Imports

import time
import json
import logging
import traceback
import discord

import requests


from discord.ext import commands
from discord.ext.commands import CommandNotFound, errors
from discord_slash import SlashCommand


from customfunctions import config, set_config
from customfunctions import CustomChecks, ErrorHandling
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
with open("storage/mutes.json", "r") as file:
	bot.mutes = json.load(file)
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
	else:
		await get_error(ctx, error)

async def get_error(ctx, error:object):
	lambda_error_handling = { # Errors that can be handled in one line of code
		errors.NotOwner                 : lambda: ctx.message.add_reaction(str('🔏')),
		errors.DisabledCommand          : lambda: ctx.message.add_reaction(str('<:DisabledCommand:804476191268536320>')),
		errors.MissingPermissions       : lambda: ctx.message.add_reaction(str('🔐')),
		errors.BotMissingPermissions    : lambda: ctx.reply("I do not have the requisite permissions"),
		errors.MissingRole              : lambda: ctx.message.add_reaction(str('🔐')),
		errors.MissingRequiredArgument  : lambda: ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`", delete_after=30),
		errors.BadArgument              : lambda: ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`", delete_after=30),
		errors.NoPrivateMessage         : lambda: ctx.message.add_reaction(str('<:ServerOnlyCommand:803789780793950268>')),
		discord.errors.Forbidden        : lambda: ctx.reply("I do not have the requisite permissions"),
		CustomChecks.IncorrectGuild     : lambda: ctx.reply(content="This command does not work in this server.", delete_after=10)
	}
	function_error_handling = { # More complicated handling that require normal functions
		errors.CommandOnCooldown        : ErrorHandling.command_on_cooldown
	}
	error_type = type(error.original) if isinstance(error, errors.CommandInvokeError) else type(error) # Get the type of the error
	if error_type in lambda_error_handling.keys(): # check if the error is in the lambda dictionary and if so, call the handling function
		await lambda_error_handling[error_type]()

	elif error_type in function_error_handling.keys(): # check if the error is in the function dictionary, and if so, call the function with arguments
		await function_error_handling[error_type](ctx, error)

	else: # if the error isn't handled, handle it with the ungaught error handler
		await uncaught_error(ctx, error)

async def uncaught_error(ctx, error):
	error_str = str(error).replace(personal_info, '')
	# Send user a message
	await ctx.message.add_reaction('<:CommandError:804193351758381086>')
	await ctx.reply("Error:\n```"+error_str+"```\nSmallPepperZ will be informed", delete_after=60)

	# Get traceback info

	lines = traceback.format_exception(type(error), error, error.__traceback__)
	traceback_text = ''.join(lines)

	# Github gist configuration
	errornum = int(config("errornum"))+1
	set_config("errornum", str(errornum))

	traceback_text = traceback_text.replace(personal_info, '')

	apiurl = "https://api.github.com/gists"
	gist_id = config("githubgist")
	githubtoken = config('githubtoken')

	payload = {"description": "SachiBot Errors - A gist full of errors for my bot",
			   "public": False,
			   "files": {
				   f"SachiBotPyError {errornum:02d}.log": {
					   "content": f'Error - {error} \n\n\n {traceback_text}'
					   }
					}
				}
	# Upload to github gist
	requests.patch(f'{apiurl}/{gist_id}',
				   headers={'Authorization': f'token {githubtoken}'},
				   params={'scope': 'gist'},
				   data=json.dumps(payload))
	# Build and send embed for error channel
	channel = bot.get_channel(errorchannel)
	embed1 = discord.Embed(
		title=f"Error {errornum:02d}", color=embedcolor)
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
									f'[SachiBotPyError {errornum:02d}.log](https://gist.github.com/SmallPepperZ/{gist_id}#file-sachibotpyerror-{errornum:02d}-log'
									f' \"Github Gist #{errornum:02d}\") ', inline='false')
	await channel.send(embed=embed1)

	ghost_ping = await channel.send('<@!545463550802395146>')
	await ghost_ping.delete()



# endregion


bot.run(token)
