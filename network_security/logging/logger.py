import logging
import os
from datetime import datetime

# Create log filename
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Logs directory
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Full log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),  # Save logs to file
        logging.StreamHandler(),             # Print logs to terminal
    ],
)

logger = logging.getLogger(__name__)

logger.info("Logger initialized successfully.")
logger.warning("This is a warning.")
logger.error("This is an error.")