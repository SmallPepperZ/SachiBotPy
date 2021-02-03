from typing import Tuple
import discord
from discord import Embed
import logging
from datetime import datetime
class EmbedMaker:
	def AddDescriptionField(embed:discord.Embed, key:str, value:str, *, boldkey:bool=True):
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

	def AddBlankField(embed:discord.Embed):
		"""Adds a line break to the description of an embed

		Parameters
		----------
		embed : discord.Embed
			The embed to add the blank line to to

		"""

		if embed.description == Embed.Empty:
			embed.__setattr__("description", f'\n')
		else:
			embed.__setattr__("description", f'{embed.description}\n')
	
	def FooterPresets(embed:discord.Embed, ctx, *presets:str, delimiter:str=" - ", customtext:str=None, customtextloc:str="prepend", customurl:str=None):
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
				Addiotional text to add to the footer, by default None
			
			customtextloc : "prepend" or "append", optional
				where to put the custom text, if applicable, by default "prepend"
			
			customurl : str, optional
				The icon url to override with, by default None
		"""
		customtextloc = customtextloc.lower()
		if not(customtextloc == "prepend" or customtextloc == "append"):
			raise ValueError(f"{customtextloc} must be either 'Append' or 'Prepend'")
		text:list = []
		if "author" in presets:
			icon_url= ctx.author.avatar_url
			text = text.append(f'Request by {ctx.author}')
		icon_url = customurl if customurl == None else None
		if "timestamp" in presets:
			text = text.append(datetime.now())
		if "channel" in presets:
			text = text.append(ctx.channel.name)
		if icon_url != None:
			embed
		else:
			return text
