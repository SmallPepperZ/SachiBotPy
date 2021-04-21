import json
from typing import Union
from discord.ext.commands import Bot
from discord import User

def find_flags(flags:list, args:Union[list, tuple]) -> "tuple[list, list]":
	"""Returns a list of flags and a list of arguments from an invocation

	Parameters
	----------
	flags : list
		The flags to check for as a list. Will be returned if they are used.
	args : list or tuple
		The arguments to search for flags in.

	Returns
	-------
	used flags : list
		A list of flags that were used in the command. If none are used, will be an empty list
	args : list
		A list of all the arguments that were not flags
	"""
	used_flags:list = []
	args = list(args)
	for flag in flags:
		if flag in args:
			args.pop(args.index(flag))
			used_flags.append(flag)
	return used_flags, args


def write_file(filepath:str, data:dict, indent:int=4) -> None:
	"""Writes a dictionary to a file

	Parameters
	----------

	filepath : str
		The path of the file to write to

	data : dict
		The dictionary to dump as json

	indent : int, optional
		The indent to use when dumping, by default 4
	"""
	with open(filepath, "w") as file:
		json.dump(data, file, indent=indent)

def read_file(filepath:str) -> dict:
	"""Gets the contents of a JSON file as a dictionary

	Parameters
	----------

	filepath : str
		The path of the file to read

	Returns
	-------

	json : dict
		The contents of the JSON file as a dictionary

	"""
	with open(filepath, "r") as file:
		return json.loads(file.read())

async def get_owner(bot:Bot) -> User:
	app_info = await bot.application_info()
	return app_info.owner
