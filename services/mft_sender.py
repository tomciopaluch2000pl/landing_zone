"""
mft_sender.py

This module simulates the action of sending a validated feed submission
to an external system via MFT (Managed File Transfer). In production,
this function can be replaced with actual MFT integration logic (e.g., API call,
command-line transfer, queue-based trigger, etc.).

Currently logs the action and emits a Grafana-compatible event.
"""

import os
from utils.logger import get_logger
from utils.grafana_logger import log_event

# Initialize logger
logger = get_logger()

def send_to_mft(submission_dir: str) -> bool:
    """
    Simulates the upload of a validated submission folder to MFT.

    Args:
        submission_dir: Path to the validated submission directory

    Returns:
        True to indicate simulated success
    """
    submission_name = os.path.basename(submission_dir)

    # In production: replace this with real MFT transfer logic
    logger.info(f"[MFT] Simulating upload of {submission_name}...")

    # Log Grafana-compatible event
    log_event("mft_sent", submission_name, "mft_transfer", "Simulated successful MFT transfer")

    return True
