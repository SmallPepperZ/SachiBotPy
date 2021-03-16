from datetime import datetime
import discord
from discord import Embed

def add_description_field(embed:discord.Embed, key:str, value:str, *, boldkey:bool=True):
	"""Adds a one line key: value field to an embed's description on a new line

	Parameters
	----------
	embed : discord.Embed
		The embed to add to

	key : str
		The key for the field

	value : str
		The value for the field

	boldkey = boldkey : bool, defaults to True
		Whether to bold the key value, set to false if there is alternate formatting.

	"""
	if boldkey:
		boldmarks = '**'
	else:
		boldmarks = ''
	if embed.description == Embed.Empty:
		embed.__setattr__("description", f'{boldmarks}{key}:{boldmarks} {value}')
	else:
		embed.__setattr__("description", f'{embed.description}\n{boldmarks}{key}:{boldmarks} {value}')

def add_blank_field(embed:discord.Embed):
	"""Adds a line break to the description of an embed

	Parameters
	----------
	embed : discord.Embed
		The embed to add the blank line to to

	"""

	if embed.description == Embed.Empty:
		embed.__setattr__("description", '\n')
	else:
		embed.__setattr__("description", f'{embed.description}\n')

def footer_presets(embed:discord.Embed, ctx, *presets:str, delimiter:str=" - ", customtext:str=None, customtextloc:str="prepend", customurl:str=None):
	"""Adds some footer presets to an embed's footer

		Parameters
		----------
		embed : discord.Embed
			The embed to set the footer on

		ctx : Context
			The context of the command invocation

		delimiter : str, optional
			What to connect the sections with, by default " - "

		customtext : str, optional
			Additional text to add to the footer, by default None

		customtextloc : "prepend" or "append", optional
			where to put the custom text, if applicable, by default "prepend"

		customurl : str, optional
			The icon url to override with, by default None
	"""
	customtextloc = customtextloc.lower()
	if customtextloc not in ("prepend", "append"):
		raise ValueError(f"{customtextloc.capitalize()} must be either 'Append' or 'Prepend'")
	text:list = []
	if "author" in presets:
		icon_url= ctx.author.avatar_url
		text = text.append(f'Request by {ctx.author}')
	icon_url = customurl if customurl is not None else None
	if "timestamp" in presets:
		text = text.append(datetime.now())
	if "channel" in presets:
		text = text.append(ctx.channel.name)
	if icon_url is not None:
		embed
	else:
		return text
