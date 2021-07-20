import json
from customfunctions.funcs import database_manager as DBManager
def get_config(item:str) -> "str|list|int":
	my_db = DBManager.Database()
	config:"list[tuple[str,str,str]]" = my_db.cursor.execute("""select * from config where key=?""", (item,)).fetchone()
	if config is None:
		raise ValueError(f'{item} not in config')
	if config[2] == "string":
		return config[1]
	if config[2] == "list":
		return json.loads(config[1])
	if config[2] == "hex":
		return int(config[1], 16)
	else:
		raise ValueError("Invalid config type")

def set_config(item:str, value:str, config_type:str="string"):
	if config_type in ("string", "hex"):
		formatted_item = str(value)
	elif config_type == "list":
		formatted_item = json.dumps(value)
	my_db = DBManager.Database()
	keys = my_db.cursor.execute("""select key from config""").fetchall()
	if item in [key[0] for key in keys]:
		my_db.cursor.execute("""UPDATE config SET value = ? WHERE key = ?""", (str(formatted_item), item))
		my_db.connection.commit()
	else:
		raise ValueError(f'{item} not in config')
	# with open('storage/config.json', 'w') as file:
	# 	json.dump(config, file, indent=4)
