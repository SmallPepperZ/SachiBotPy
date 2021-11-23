import datetime


def parse(value:str) -> int:
	"""Converts a string like '10m' into seconds

	Parameters
	----------
	value : str
		The string to convert. Can have s (seconds), m (minutes), h (hours), or d (days)

	Returns
	-------
	int
		The number of seconds represented by the input string
	"""
	scale_key = {
		"s": 1,
		"m": 60,
		"h": 3600,
		"d": 86400
	}
	scale_letter = value[-1]

	if scale_letter in scale_key.keys():
		scale = scale_key[scale_letter]
	else:
		raise ValueError("Time scale not recognized")

	try:
		seconds =  int(''.join(list(value)[:-1]))
	except ValueError as err:
		raise ValueError("Invalid time") from err
	return seconds*scale


def get_future_time(seconds:int) -> datetime.datetime:
	"""Adds the specified number of seconds to the current time

	Parameters
	----------
	seconds : int
		The number of seconds to add

	Returns
	-------
	datetime.datetime
		The new time with the seconds added
	"""

	current_time = datetime.datetime.now()
	new_time = current_time+datetime.timedelta(0, seconds)
	return new_time
