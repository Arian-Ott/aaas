import logging
from colorlog import ColoredFormatter
from api.core.deps import settings

def setup_logging(prod: bool = True) -> None:
    # Create a colored formatter for log messages
    formatter = ColoredFormatter(
        "%(log_color)s - %(levelname)s - %(message)s",
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red',
        }
    )
    
    # Create a stream handler with the colored formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    # Clear any existing handlers from Uvicorn loggers
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
    
    # Set up basic configuration using the handler
    logging.basicConfig(
        level=logging.DEBUG if not settings.PROD else logging.INFO,
        handlers=[handler]
    )