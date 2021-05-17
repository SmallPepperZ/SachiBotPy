import json
def get_config(item:str):
	with open('storage/config.json') as file:
		config = json.load(file)
	if item in config.keys():
		return config[item]
	else:
		raise ValueError(f'{item} not in config')

def set_config(item:str, value:str):
	with open('storage/config.json') as file:
		config = json.load(file)
	if item in config.keys():
		config[item] = value
	else:
		raise ValueError(f'{item} not in config')
	with open('storage/config.json', 'w') as file:
		json.dump(config, file, indent=4)
