"""
process_loaders.py

Description:
This module processes configuration entries and delegates loading to specific loader functions.

Author: Kyrill Meyer
Version: 0.0.1
Creation Date: June 10, 2025
"""

import keyboard
import logging
import threading
from globals import stop_loading
from loaders.directory_loader import load_from_directory
from loaders.csv_loader import load_from_csv

#
# initialize logger
logger = logging.getLogger("Learn2RAGImporter")

# function wathing the ESC key
def monitor_esc_key():
    """
    Monitor the ESC key and set the stop_loading flag when pressed.
    """
    global stop_loading
    keyboard.wait("esc")  # waiting for ESC
    stop_loading = True
    logger.info("ESC key pressed. Aborting loading process...")
    raise KeyboardInterrupt("Process interrupted by user via ESC key.")

def process_configuration_entries(config_entries):
    """
    Process configuration entries and load documents based on loader type.

    Args:
        config_entries (list): List of configuration entries.

    Returns:
        list: List of loaded documents.
    """

    all_documents = []

    # Starting monitoring thread
    esc_thread = threading.Thread(target=monitor_esc_key, daemon=True)
    esc_thread.start()

    for entry in config_entries:
        loader_type = entry.get("loader_type")
        path = entry.get("path")
        recursive = entry.get("recursive", False)

        if not loader_type or not path:
            logger.error(f"Invalid configuration entry: {entry}")
            continue

        try:
            logger.info(f"Processing entry: {entry}, please wait...")
            if loader_type == "DirectoryLoader":
                documents = load_from_directory(path, recursive=recursive)
            elif loader_type == "CSVLoader":
                documents = load_from_csv(path)
            else:
                logger.error(f"Unknown loader type: {loader_type}")
                continue

            logger.info(f"Loaded {len(documents)} documents from {path} using {loader_type}.")
            all_documents.extend(documents)
        except Exception as e:
            logger.error(f"Error processing entry {entry}: {e}")

    return all_documents

