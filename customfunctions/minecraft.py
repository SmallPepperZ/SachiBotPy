from typing import Tuple
import requests, json
from discord.ext.commands import CommandError
usertoken = "474005"
class ExpiredMcToken(CommandError):
	pass
class InvalidMcServer(CommandError):
	pass
def link_discord_mc(usertoken:int) -> Tuple[str, str]:
	"""Links a minecraft account with a discord user via their usertoken

	Parameters
	----------
	usertoken : int
		a 6 digit number given by the minecraft server

	Returns
	-------
	uuid : str
		The minecraft uuid of the user's linked account
	
	username : str
		The minecraft username of the user's linked account

	Raises
	------
	ExpiredMcToken
		If the usertoken given is expired, this is raised
	"""
	usertoken = str(usertoken)
	if len(usertoken) == 6:
		headers   = {'token': usertoken}
		res       = requests.get("https://mc-oauth.net/api/api?token", headers=headers)
		res       = json.loads(res.text)
		if res["status"] == 'success':
			return res["uuid"], res["username"]
		else:
			raise ExpiredMcToken(res["message"])
	else:
		print("Invalid length")
def query_mc_server(*, ip:str, port:int=25565) -> dict:
	"""Gets information from a minecraft server

	Keyword Arguments
	----------
	ip = ip: str
		The IP of the server to query

	port = 25565 : int, optional
		The port of the server to query, by default 25565

	Returns
	-------
	serverinfo : dict
		Structured below:

		{
		  "MaxPlayers": int,
		  "MOTD": str,
		  "Playerlist": list, 
		  "Players": int, 
		  "Plugins": list, 
		  "Software": str, 
		  "Version": str, 
		  "Status": str
		}

	Raises
	------
	InvalidMcServer
			This is raised if the server ip or port is invalid

	TimeoutError
		This is raised if the query took too long

	CommandError
		This is raised as a generic error response
	"""
	res = requests.get(f"https://api.minetools.eu/query/{ip}/{port}")
	res = json.loads(res.text)
	if res["status"] == "ERR":
		if res["error"] == "[Errno -2] Name or service not known":
			raise InvalidMcServer
		elif res["error"] == "timed out":
			raise TimeoutError
		else:
			raise CommandError(res["error"])
	return res
	
