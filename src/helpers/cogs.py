def format_cog_name(cog_name:str) -> str:
	return cog_name.replace('cogs.', '').replace('_', ' ').title().replace('.','/')