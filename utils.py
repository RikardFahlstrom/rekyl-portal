import configparser
import logging


def load_config_file() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read("config.ini")
    logging.info("Successfully loaded config file")

    return config


def setup_logging():
    logging.basicConfig(
        filename="app.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
