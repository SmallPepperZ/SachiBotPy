
import json
import traceback
import requests
from discord.ext import commands
import discord
from utils import config, set_config

errorchannel = int(config("errorchannel"))
personal_info = config("pathtohide")
embedcolor = config("embedcolor")

async def command_on_cooldown(ctx, error):
	await ctx.message.add_reaction(str('<:Cooldown:804477347780493313>'))
	if str(error.cooldown.type.name) != "default":
		cooldowntype = f'per {error.cooldown.type.name}'
	else:
		cooldowntype = 'global'
		await ctx.reply(f"This command is on a {round(error.cooldown.per, 0)}s {cooldowntype} cooldown. "
						f"Wait {round(error.retry_after, 1)} seconds",
						delete_after=min(10, error.retry_after))

async def invalid_invocation(ctx, error): #pylint:disable=unused-argument
	command:commands.Command = ctx.command
	if command.help is not None:
		await ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`\n\nHelp: {command.help}", delete_after=30)
	else:
		await ctx.reply(f"Missing required argument!\nUsage:`{ctx.command.signature}`", delete_after=30)

async def uncaught_error(ctx, error, bot:discord.Client, silent:bool=False):
	error_str = str(error).replace(personal_info, '')
	# Send user a message
	if not silent:
		await ctx.message.add_reaction('<:CommandError:804193351758381086>')
		try:
			await ctx.reply(f"Error:\n```{error_str}```\n{bot.owner.name} will be informed", delete_after=60)
		except discord.errors.HTTPException:
			await ctx.reply(f"An error occurred. {bot.owner.name} will be informed")

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
	ghost_ping = await channel.send(f'<@!{bot.owner.id}>')
	await ghost_ping.delete()
