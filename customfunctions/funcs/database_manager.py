import sqlite3

databases = {
	"storage":"storage/SachiBotStorage.db",
	"mee6":"storage/mee6.db",
	"messages": "storage/DiscordMessages.db"
}

class Database():
	def __init__(self, database_name:str="storage"):
		"""Makes a connection and cursor for a database

		Parameters
		----------
		database_name : str, optional
			the database to get, by default "storage". Can be "storage", "mee6" or "messages"

		Raises
		------
		KeyError
			If the database name is not recognized
		"""
		try:
			database_path = databases[database_name]
		except KeyError as error:
			raise KeyError("Invalid database name") from error
		self.connection = sqlite3.connect(database_path)
		self.cursor = self.connection.cursor()
		self.name = database_name
