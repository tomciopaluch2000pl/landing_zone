"""
main.py

Entry point for the Landing Zone Feed Validator.
This script scans the incoming folder for .tar feed submissions, unpacks each,
validates structure and content, applies auto-fixes if enabled, and routes them
to either ready_for_mft/ or rejected/ folders based on validation results.
Logs high-level events for Grafana and ServiceNow integration.
"""

import os
import shutil
from unpacker import unpack_tar
from handlers.feed_analyzer import analyze_feed
from services.mft_sender import send_to_mft
from utils.logger import get_logger

# Initialize the application logger
logger = get_logger()

# Define input/output directories
INCOMING_DIR = "./incoming"
REJECTED_DIR = "./rejected"
READY_DIR = "./ready_for_mft"

# Ensure required directories exist
os.makedirs(REJECTED_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

def process_all_tars():
    """
    Process all .tar files in the incoming directory.
    For each file:
    - unpack it
    - analyze the feed
    - move to ready or rejected
    - log results
    """
    if not os.path.exists(INCOMING_DIR):
        logger.error(f"Incoming directory '{INCOMING_DIR}' does not exist.")
        return

    tar_files = [f for f in os.listdir(INCOMING_DIR) if f.endswith(".tar")]

    if not tar_files:
        logger.info("No .tar files found in incoming directory.")
        return

    for tar_name in tar_files:
        tar_path = os.path.join(INCOMING_DIR, tar_name)
        logger.info(f"Processing TAR file: {tar_name}")

        # Step 1: Unpack the feed submission
        submission_dir = unpack_tar(tar_path)
        if not submission_dir:
            logger.error(f"Unpacking failed for {tar_name}")
            continue

        # Step 2: Validate the feed
        success = analyze_feed(submission_dir)

        # Step 3: Route based on result
        if success:
            final_path = os.path.join(READY_DIR, os.path.basename(submission_dir))
            shutil.move(submission_dir, final_path)
            send_to_mft(final_path)  # Optional step: simulate MFT transfer
        else:
            rejected_path = os.path.join(REJECTED_DIR, os.path.basename(submission_dir))
            shutil.move(submission_dir, rejected_path)

if __name__ == "__main__":
    process_all_tars()
