import os
import shutil
from unpacker import unpack_tar
from handlers.feed_analyzer import analyze_feed
from services.mft_sender import send_to_mft
from utils.logger import get_logger

logger = get_logger()

INCOMING_DIR = "./incoming"
REJECTED_DIR = "./rejected"
READY_DIR = "./ready_for_mft"

os.makedirs(REJECTED_DIR, exist_ok=True)
os.makedirs(READY_DIR, exist_ok=True)

def process_all_tars():
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

        submission_dir = unpack_tar(tar_path)
        if not submission_dir:
            logger.error(f"Unpacking failed for {tar_name}")
            continue

        success = analyze_feed(submission_dir)
        if success:
            final_path = os.path.join(READY_DIR, os.path.basename(submission_dir))
            shutil.move(submission_dir, final_path)
            send_to_mft(final_path)
        else:
            rejected_path = os.path.join(REJECTED_DIR, os.path.basename(submission_dir))
            shutil.move(submission_dir, rejected_path)

if __name__ == "__main__":
    process_all_tars()
