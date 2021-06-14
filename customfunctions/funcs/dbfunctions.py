
def make_placeholder(table:str, dictionary:dict):
	"""Returns an SQLite string from the input dictionary

	Parameters
	----------
	table: str
		Which table of the database to insert to
	dictionary : dict
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
	columns = tuple(dictionary.keys())
	valueplaceholder = '?'
	for item in range(len(columns)-1):
		valueplaceholder += ', ?'
	sql  = f"INSERT or REPLACE into {table} {columns} values ({valueplaceholder})"
	return sql
