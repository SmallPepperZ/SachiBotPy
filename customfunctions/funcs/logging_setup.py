import logging

parentlogger = logging.getLogger("SachiBot")


def handler_maker(filepath:str,name:str,level:int, formatter:logging.Formatter) -> logging.FileHandler:
	handler = logging.FileHandler(filepath)
	handler.set_name(name)
	handler.setLevel(level)
	handler.setFormatter(formatter)
	return handler



my_formatter = logging.Formatter(style="{", fmt="{asctime} - {name} [{levelname}] {message}")
class Handlers():
	ERROR    = handler_maker("SachiBot.error.log", "SachiBotError", logging.ERROR, my_formatter)
	INFO     = handler_maker("SachiBot.info.log" , "SachiBotInfo" , logging.INFO , my_formatter)
	DEBUG    = handler_maker("SachiBot.debug.log", "SachiBotDebug", logging.DEBUG, my_formatter)


parentlogger.addHandler(Handlers.INFO)
parentlogger.addHandler(Handlers.DEBUG)
parentlogger.addHandler(Handlers.ERROR)
parentlogger.setLevel(logging.DEBUG)
