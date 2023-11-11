import logging

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def setup_logger(log_level: str):
    # Create a logger
    logger = logging.getLogger()

    logger.setLevel(LOG_LEVELS.get(log_level, logging.INFO))
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a handler and set the formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger