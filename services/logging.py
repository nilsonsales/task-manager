import logging
import streamlit as st

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def setup_logger():
    # Create a logger
    logger = logging.getLogger()

    LOG_LEVEL = st.secrets["logging"].get("LOG_LEVEL", "INFO")
    logger.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))

    FORMATTER = st.secrets["logging"].get("FORMATTER", "%(asctime)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter(FORMATTER)

    # Create a handler and set the formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger