import os
import tarfile
from utils.logger import get_logger

logger = get_logger()

def extract_submission_base_name(tar_path: str) -> str:
    base = os.path.basename(tar_path)
    return base[:-4] if base.endswith(".tar") else base

def unpack_tar(tar_path: str, destination_root: str = "./workspace") -> str:
    if not os.path.exists(tar_path):
        logger.error(f"TAR file does not exist: {tar_path}")
        return ""

    submission_name = extract_submission_base_name(tar_path)
    dest_dir = os.path.join(destination_root, submission_name)
    os.makedirs(dest_dir, exist_ok=True)

    try:
        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(path=dest_dir)
        logger.info(f"Successfully unpacked {tar_path} to {dest_dir}")
        return dest_dir
    except Exception as e:
        logger.exception(f"Failed to unpack {tar_path}: {e}")
        return ""
