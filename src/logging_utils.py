import logging
import datetime
import os

log_folder = datetime.datetime.now().strftime("log_%d_%m_%H_%M_%S")
os.makedirs(os.path.join("logs", log_folder), exist_ok=True)

def get_logger(logger_name, level=logging.INFO, to_file=False):
    """
    Creates and returns a logger with the specified name and level.
    """
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    # Remove all handlers associated with this logger to avoid duplicate messages
    logger.handlers = []

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(levelname)s: %(message)s", datefmt="%y-%m-%d %H:%M:%S"
    )

    if not to_file:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    else:
        # File handler
        os.makedirs(f"logs/{log_folder}", exist_ok=True)
        file_handler = logging.FileHandler(f"logs/{log_folder}/{log_folder}.txt", encoding="utf-8", errors='replace')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class FeatureLogger:
    def __init__(self):
        self.log_folder = os.path.join("logs", log_folder)
        # if not os.path.exists(log_folder):
        #     os.makedirs(log_folder)
        pass
    
    def log_value(self, feature_name, value):
        file_path = os.path.join(self.log_folder, feature_name + ".txt")
        with open(file_path, 'a', encoding='utf-8', errors='replace') as file:
            file.write(str(value) + "\n" + "###" + "\n")
