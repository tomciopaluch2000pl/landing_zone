import os
from utils.logger import get_logger
from utils.grafana_logger import log_event

logger = get_logger()

def send_to_mft(submission_dir: str) -> bool:
    submission_name = os.path.basename(submission_dir)
    logger.info(f"[MFT] Simulating upload of {submission_name}...")
    log_event("mft_sent", submission_name, "mft_transfer", "Simulated successful MFT transfer")
    return True
