import os
import glob
from utils.logger import get_logger
from utils.grafana_logger import log_event

logger = get_logger()

def fix_submission(submission_path: str, base_name: str) -> bool:
    fixed = False

    control_path = os.path.join(submission_path, f"{base_name}.control")
    if os.path.exists(control_path):
        size = os.path.getsize(control_path)
        if size != 0:
            with open(control_path, "w") as f:
                f.write("")
            logger.info(f"[{base_name}] Fixed: control file was not empty.")
            log_event("autofix_applied", base_name, "control_file_fix", "Reset control file to 0 bytes")
            fixed = True

    data_files = glob.glob(os.path.join(submission_path, f"{base_name}.U*.data"))
    for file_path in data_files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
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
