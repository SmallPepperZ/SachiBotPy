from urllib import parse
from discord import integrations
import requests
import json
from discord.ext.commands import CommandError

class InvalidMcServer(CommandError):
	pass

class MinecraftUser():
	def __init__(self, user:str) -> None:
		"""Gets a minecraft user

		Parameters
		----------
		user : str
			A username or UUID
		"""
		username_data:"list[dict[str, str]]" = requests.post("https://api.mojang.com/profiles/minecraft",json=[user]).json()
		if len(username_data) == 1:
			self.uuid:str = username_data[0]["id"]
			self.name:str = username_data[0]["name"]
			return
		safe_uuid = parse.quote(user)
		uuid_data:"list[dict[str, str]]|dict[str]" = requests.get(f"https://api.mojang.com/user/profiles/{safe_uuid}/names").json()
		if isinstance(uuid_data, list):
			self.uuid:str = safe_uuid
			self.name:str = uuid_data[0]["name"]
			return
		elif isinstance(uuid_data, dict) and "error" in uuid_data.keys():
			raise ValueError("Bad UUID/Username")

	@property
	def profile(self) -> "dict[str,str | list[dict[str,str]]]":
		return requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{self.uuid}').json()

	@property
	def name_history(self) -> "list[dict[str,str|int]]":
		return requests.get(f'https://api.mojang.com/user/profiles/{self.uuid}/names').json()


	def get_skin(self, skin_format:str="avatar", helm:bool=True) -> str:
		"""Gets a user's skin in different formats

		Parameters
		----------

		skin_format : str, optional
			How to render the skin, by default "avatar". Can be "avatar", "head_render", "body_render", "skin", or "cape"

		helm : bool, optional
			Whether to show the secondary layer of the skin, like the hat

		Returns
		---------
		url : str
			The URL to the minecraft skin

		"""
		skin_formats = {
			"avatar": f'https://crafatar.com/avatars/{self.uuid}{"?overlay" if helm else ""}',
			"head_render": f'https://cravatar.eu/{"helm" if helm else ""}head/{self.uuid}',
			"body_render": f'https://crafatar.com/renders/body/{self.uuid}{"?overlay" if helm else ""}',
			"skin": f'https://crafatar.com/skins/{self.uuid}',
			"cape": f'https://crafatar.com/capes/{self.uuid}'
		}
		if skin_format not in skin_formats.keys():
			raise ValueError("Unrecognized skin format")
		return skin_formats[skin_format]
				


class MinecraftServer():
	ip:str = None
	port:int = None
	online:bool = None
	motd: "list[str]" = None
	version:str = None
	world:str = None
	software:str = None
	plugins:"list[str]" = None
	mods:"list[str]" = None

	

	def __init__(self, ip:str, port:int=25565) -> None:
		self.ip = ip
		self.port = port
		data = requests.get(f"https://api.mcsrvstat.us/2/{ip}:{port}").json()
		self.online = data["online"]
		if self.online:
			
			self.players = _Players(data)
			self.motd = data["motd"]["clean"]
			self.version = data["version"]
			if "map" in data.keys():
				self.world = data["map"]
			if "software" in data.keys():
				self.software = data["software"]
			
			if "plugins" in data.keys():				
				self.plugins = data["plugins"]["names"]
			if "mods" in data.keys():
				self.mods = data["mods"]["names"]

	@property
	def server_icon(self) -> str:
		"""Returns the url to the server icon as a png"""
		return f"https://api.mcsrvstat.us/icon/{self.ip}:{self.port}"

	@property
	def color(self) -> int:
		"""Returns 0xFF0000 if the server is offline and 0x00FF00 if it is online"""
		if self.online:
			return 0x00FF00
		else:
			return 0xFF0000

class _Players():
	names    : "list[str]"     = None
	uuids    : "dict[str,str]" = None
	max      : int             = None
	count    : int             = None

	def __init__(self, data):
		self.max = data["players"]["max"]
		self.count = data["players"]["online"]
		if "uuid" in data["players"].keys():
			self.uuids = data["players"]["uuid"]
			self.names = data["players"]["list"]

print(MinecraftServer("mc.hypixel.net").players.uuids)