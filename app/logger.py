# logger.py

import logging
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

LOG_FILE = os.path.join(log_dir, "app.log")

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(),
        ]
    )
