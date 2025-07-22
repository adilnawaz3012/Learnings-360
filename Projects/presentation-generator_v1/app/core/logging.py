import logging
from loguru import logger

def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logger.add(
        "app.log",
        rotation="100 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )