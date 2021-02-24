def find_flags(flags:list, args):
	"""Returns a list of flags and a list of arguments from an invocation

	Parameters
	----------
	flags : list
		The flags to check for as a list. Will be returned if they are used.
	args : list or tuple
		The arguments to search for flags in.

	Returns
	-------
	used flags : list
		A list of flags that were used in the command. If none are used, will be an empty list
	args : list
		A list of all the arguments that were not flags
	"""
	used_flags:list = []
	args = list(args)
	for flag in flags:
		if flag in args:
			args.pop(args.index(flag))
			used_flags.append(flag)
	return used_flags, args