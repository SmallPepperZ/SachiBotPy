
import time
import json
import discord
import traceback


from discord.ext import commands
from discord.ext.commands import CommandNotFound, errors
from discord.mentions import AllowedMentions

from utils.funcs import handling #pylint:disable=unused-import
from utils import CustomChecks, ErrorHandling, StatusManager
from utils import master_logger

from helpers import config

from cogs import utility

COGS = [	
        'cogs.owner.config.color',
		'cogs.cog.reload'
       ] + utility.cogs




start_time_local = time.time()

intents = discord.Intents.all()
intents.typing = False
bot = commands.Bot(command_prefix=config.prefix,
				   intents=intents,
				   case_insensitive=True)

bot.allowed_mentions=AllowedMentions(everyone=False,roles=False)

errorchannel = int(config.errorchannel)

bot.start_time = start_time_local

print(COGS)

bot.remove_command('help')

startup_cogs = ''
if __name__ == '__main__':
	def format_cog_name(cog_name:str) -> str:
			return cog_name.replace('cogs.', '').replace('_', ' ').title().replace('.','/')

	
	startup_lines = []
	
	for extension in COGS:
		try:
			bot.load_extension(extension)
			startup_lines.append(f'<:Success:865674863330328626> | {format_cog_name(extension)}')
		except Exception as error:
			startup_lines.append(f'<:Failure:865674863031877663> | {format_cog_name(extension)}')
			for line in traceback.format_exception(type(error), error, error.__traceback__):
				master_logger.error(line)
	startup_cogs = "\n".join(startup_lines)
	


logger = master_logger.getChild("main")



@bot.event
async def on_ready():
	logger.info("Bot initialized")
	await StatusManager.apply_status(bot)
	startup_channel:discord.TextChannel = bot.get_guild(797308956162392094).get_channel(867140356424466448)
	await startup_channel.send(embed=discord.Embed(color=config.embedcolor,title="Startup", description=startup_cogs))

	bot.owner = (await bot.application_info()).owner
	bot.prefix = config.prefix


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
	error_handling = { # Errors that can be handled in one line of code
		errors.NotOwner                 : lambda: ctx.message.add_reaction(str('🔏')),
		errors.DisabledCommand          : lambda: ctx.message.add_reaction(str('<:DisabledCommand:804476191268536320>')),
		errors.MissingPermissions       : lambda: ctx.message.add_reaction(str('🔐')),
		errors.BotMissingPermissions    : lambda: ctx.reply("I do not have the requisite permissions"),
		errors.MissingRole              : lambda: ctx.message.add_reaction(str('🔐')),
		errors.MissingRequiredArgument  : lambda: ErrorHandling.invalid_invocation(ctx,error),
		errors.BadArgument              : lambda: ErrorHandling.invalid_invocation(ctx,error),
		errors.NoPrivateMessage         : lambda: ctx.message.add_reaction(str('<:ServerOnlyCommand:803789780793950268>')),
		discord.errors.Forbidden        : lambda: ctx.reply("I do not have the requisite permissions"),
		CustomChecks.IncorrectGuild     : lambda: ctx.reply(content="This command does not work in this server.", delete_after=10),
		errors.CommandOnCooldown        : lambda: ErrorHandling.command_on_cooldown(ctx,error)
	}

	error_type = type(error.original) if isinstance(error, errors.CommandInvokeError) else type(error) # Get the type of the error
	if error_type in error_handling.keys(): # check if the error is in the dictionary dictionary and if so, call the handling function
		await error_handling[error_type]()
	else: # if the error isn't handled, handle it with the uncaught error handler
		await ErrorHandling.uncaught_error(ctx, error, bot)



bot.run(config.discordtoken)
