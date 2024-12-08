import logging
import os
import signal
import sys
# Centralized logger setup
def setup_logger():
    logger = logging.getLogger('Genmaya3sLogger')
    if not logger.hasHandlers():  # Prevent adding multiple handlers
        logger.setLevel(logging.DEBUG)

        # Define log file path outside the folders
        log_file_path = os.path.join(os.path.dirname(__file__), 'genmaya3s.log')

        # File handler
        file_handler = logging.FileHandler(log_file_path, mode='a')  # Append mode
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        # Console handler (optional for debugging in the terminal)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

    return logger

def cleanup_logger():
    logger = logging.getLogger('Genmaya3sLogger')
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)

    log_file_path = os.path.join(os.path.dirname(__file__), 'genmaya3s.log')
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        print("Log file deleted successfully.")
    else:
        print("Log file does not exist.")

def signal_handler(signal, frame):
    print('Ctrl+C pressed! Cleaning up...')
    cleanup_logger()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
logger = setup_logger()