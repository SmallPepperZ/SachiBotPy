from typing import Tuple
import logging
import os
import requests, json
from requests.exceptions import Timeout
from discord.ext import commands
import datetime, pytz
from datetime import timedelta, datetime
import sqlite3

dbpath = "storage/mee6.db"
dbcon = sqlite3.connect(str(dbpath))
dbcur = dbcon.cursor()

class PlayerNotFound(commands.CommandError):
	pass



def get_user(userid:int, *, pages:int=3, limit:int=500, guildid:int=302094807046684672, nocache:bool=False) -> Tuple[int, int]:
	"""Gets a user's mee6 information for a guild

		Parameters
		----------
		userid : int
			The user id to search for

		pages = 3 : int, optional
			Number of pages to search, by default 3

		limit = 500: int, optional
			Number of users per page, by default 500

		guildid = 302094807046684672: int, optional
			Guildid to search, by default 302094807046684672
		
		nocache = False: bool, optional
			Whether to ignore the mee6 cache, by default False
		
		Returns
		-------
		level : int
			The user's level in the specified guild, between 1 and 1000

		messages : int
			The user's messages in the guild, counted by mee6

		Raises
		------
		PlayerNotFound
			Returns if the member can not be found in searched pages
	"""
	if not (1 <= limit <= 1000):
		raise ValueError("Limit must be between 1 and 1000")
	api       = "https://mee6.xyz/api/plugins/levels/leaderboard/"#?page = 2&limit = 500
	cachedate = datetime.fromtimestamp(os.path.getmtime('storage/mee6.db'))
	yesterday = datetime.now() - timedelta(hours = 1)
	player    = None

	with dbcon:
		info = dbcur.execute("select * from members where id=?", [userid])
	player = info.fetchone()
	#if cache is a day old or player not found in existing cache, remake it
	if cachedate < yesterday or player == None or nocache:
		print("Player not in cache, or cache outdated")
		people = []
		for page in range(pages):
			
			#Make request, timeout in case it gets stuck
			try:
				response = requests.get(f'{api}{guildid}?page={page}&limit={limit}', timeout=20)
			except Timeout:
				try:
					response = requests.get(f'{api}{guildid}?page={page}&limit={limit}', timeout=20)
				except Timeout:
					raise
			print(page)
			pagejson = json.loads(response.text)
			players  = pagejson["players"]
			player   = None
			#get player with id
			for playerdict in players:
				playerid = playerdict["id"]
				messages = playerdict["message_count"]
				level = playerdict["level"]
				tuple = (playerid, messages, level)
				people.append(tuple)
				if playerid == str(userid):
					player = (playerid, messages, level)
					break
			if player != None:
				break

		# Fill the table
		with dbcon:
			dbcon.execute("delete from members").rowcount		
			dbcon.executemany("insert into members(id, messages, level) values (?,?,?)", people)
		if player == None:
			raise PlayerNotFound("User could not be found")
	else:
		print("Player in cache")
	return player[1], player[2]
	