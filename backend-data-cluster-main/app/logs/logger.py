import sys
from loguru import logger
import logging

# Configure logger
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_error.disabled = True
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = True
format = "[{time}]: {level} : {name}:{function}:{line} : {message} {exception}"
logger.remove()
logger.add(sys.stdout, level="INFO", format=format, enqueue=True, colorize=True)

# Returns the configured logger
def get_logger():
    return logger