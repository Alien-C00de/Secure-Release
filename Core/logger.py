import logging
import sys

def setup_logger(name="cicdsec", config=None):
    import os

    level = logging.INFO
    if config:
        level_name = config.get("logging", {}).get("level", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%H:%M:%S")
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if config and config.get("logging", {}).get("to_file", False):
            log_path = config["logging"].get("log_file", "security.log")
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    logger.propagate = False
    return logger
