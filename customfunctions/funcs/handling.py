import sys
from types import TracebackType
from typing import Type
import traceback as traceback_lib
from customfunctions import master_logger

def error_handling(exctype:Type[BaseException], value:BaseException, traceback:TracebackType):
	try:
		# Format the exception
		traceback_lines = traceback_lib.format_exception(exctype, value, traceback)
		# Make each line a value in the list
		traceback_lines = (''.join(traceback_lines)).split("\n")
		# Filter out empty strings
		traceback_lines = [line for line in traceback_lines if line != ""]
		for line in traceback_lines:
			master_logger.error(line)
	except:
		sys.__excepthook__(exctype,value,traceback)
sys.excepthook = error_handling
