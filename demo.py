from src.logger import logging

logging.debug("This is a debug message")

from src.exception import MyException
import sys
try:
    a = 1/0
except Exception as e:
    raise MyException(e,sys) from e