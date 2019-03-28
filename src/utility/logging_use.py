# -*- coding: utf-8 -*-
import yaml
import logging.config
CONFIG_FILE = "logging_config.yaml"
with open(CONFIG_FILE,"r",encoding="utf-8") as f:
    config = yaml.load(f)
    logging.config.dictConfig(config)

logging.critical("a")
logging.exception("Failed to open sklearn.txt from logger.exception")