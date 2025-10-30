import sys

from loguru import logger
from franklin_client.config import settings

logger.remove()  # Remove the default logger
logger.add(sys.stderr, level=settings.log_level, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
