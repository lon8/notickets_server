from loguru import logger
import sys

def configure_logger() -> None:
    logger.remove()
    logger.add(sink='logs/logs.log',
               format="{time} {level} {message}",
               level='INFO',
               retention="10 days",
               rotation="10 MB")
    
    logger.add(sys.stderr, format="<green>{time}</green> <level>{level}</level> <cyan>{message}</cyan>", level="DEBUG", colorize=True)

    logger.info("Logger configured")