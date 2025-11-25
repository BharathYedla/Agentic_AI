import logging
import sys
from core.config import settings

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set log levels for third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
