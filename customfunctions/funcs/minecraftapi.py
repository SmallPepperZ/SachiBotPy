from urllib import parse
import requests


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

	def skin(self, skin_format:str="avatar", helm:bool=True) -> str:
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
			"head_render": f'https://crafatar.com/renders/head/{self.uuid}{"?overlay" if helm else ""}',
			"body_render": f'https://crafatar.com/renders/body/{self.uuid}{"?overlay" if helm else ""}',
			"skin": f'https://crafatar.com/skins/{self.uuid}',
			"cape": f'https://crafatar.com/capes/{self.uuid}'
		}
		if skin_format not in skin_formats.keys():
			raise ValueError("Unrecognized skin format")
		return skin_formats[skin_format]

print(MinecraftUser("jeb_").profile)
