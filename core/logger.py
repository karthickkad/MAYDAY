"""
logger.py

Logging module for MAYDAY.
"""

import logging
import os


class Logger:

    LOG_DIRECTORY = "logs"
    LOG_FILE = "mayday.log"

    @classmethod
    def setup(cls):
        """
        Configure the application logger.
        """

        os.makedirs(cls.LOG_DIRECTORY, exist_ok=True)

        log_path = os.path.join(cls.LOG_DIRECTORY, cls.LOG_FILE)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def warning(message):
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def debug(message):
        logging.debug(message)