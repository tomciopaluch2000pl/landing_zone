"""
logger.py

Initializes and configures the application-wide logger.
Logs messages both to console and to a rotating file (app.log).
Used by all modules for consistent logging output.
"""

import logging
import os

def get_logger():
    """
    Returns a configured logger instance for the app.
    Logs are written to logs/app.log and also displayed in the console.
    
    Returns:
        logging.Logger instance
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path),       # Log to file
            logging.StreamHandler()              # Log to stdout
        ]
    )

    return logging.getLogger("landingzone")
