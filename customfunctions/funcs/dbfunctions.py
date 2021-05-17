class DatabaseFromDict():
	def make_placeholder(table:str, dict:dict, *, operation:str='insert'):
		"""Returns an SQLite string from the input dictionary

		Parameters
		----------
		table: str
			Which table of the database to insert to
		dict : dict
			The dictionary with the data, uses the keys as columns

		Keyword Parameters
		------------------
		operation:str = insert
			Which operation to use, by default, insert

		Returns
		-------
		str
			An SQLite command to use with `dbcon.executemany`
		"""
		columns = tuple(dict.keys())
		valueplaceholder = '?'
		for item in range(len(columns)-1): valueplaceholder += ', ?'
		sql  = f"insert or replace into {table} {columns} values ({valueplaceholder})"
		return sql