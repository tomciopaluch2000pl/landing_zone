"""
auto_fixer.py

Performs basic automated corrections on known validation issues within a feed submission.
Examples include:
- Resetting non-empty control files to 0 bytes
- Adding missing headers to .data files

Used when AUTO_FIX_ENABLED is enabled in the analyzer.
"""

import os
import glob
from utils.logger import get_logger
from utils.grafana_logger import log_event

# Initialize logger
logger = get_logger()

def fix_submission(submission_path: str, base_name: str) -> bool:
    """
    Applies basic auto-fixes to a feed submission directory.

    Args:
        submission_path: Path to unpacked submission folder
        base_name: Base name used for identifying files in the submission

    Returns:
        True if any fixes were applied, False if nothing changed
    """
    fixed = False

    # --- Fix 1: Control file must be 0 bytes ---
    control_path = os.path.join(submission_path, f"{base_name}.control")
    if os.path.exists(control_path):
        size = os.path.getsize(control_path)
        if size != 0:
            with open(control_path, "w") as f:
                f.write("")
            logger.info(f"[{base_name}] Fixed: control file was not empty.")
            log_event("autofix_applied", base_name, "control_file_fix", "Reset control file to 0 bytes")
            fixed = True

    # --- Fix 2: Add header to .U*.data files if missing ---
    data_files = glob.glob(os.path.join(submission_path, f"{base_name}.U*.data"))
    for file_path in data_files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Simple heuristic: no letters in the first line likely means missing header
        if lines and not any(char.isalpha() for char in lines[0]):
            num_cols = len(lines[0].split(";"))
            header = ";".join([f"COL{i+1}" for i in range(num_cols)]) + "\n"
            lines.insert(0, header)

            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            logger.info(f"[{base_name}] Fixed: added missing header to {os.path.basename(file_path)}")
            log_event("autofix_applied", base_name, "header_fix", f"Header added to {os.path.basename(file_path)}")
            fixed = True

    return fixed
