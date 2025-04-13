"""
unpacker.py

Responsible for unpacking incoming .tar archive submissions into a working directory.
Each .tar file is expected to contain one feed submission folder, which will be unpacked
under workspace/<submission_name>/ for further validation and processing.
"""

import os
import tarfile
from utils.logger import get_logger

# Initialize logger
logger = get_logger()

def extract_submission_base_name(tar_path: str) -> str:
    """
    Extract the base name of the submission from the TAR file name.
    Assumes file format: <base_name>.tar
    """
    base = os.path.basename(tar_path)
    return base[:-4] if base.endswith(".tar") else base

def unpack_tar(tar_path: str, destination_root: str = "./workspace") -> str:
    """
    Unpacks a .tar file into a subdirectory under the workspace directory.

    Args:
        tar_path: Path to the .tar archive to unpack
        destination_root: Root folder for unpacked contents (default: ./workspace)

    Returns:
        Full path to the unpacked directory, or empty string if failure occurred
    """
    if not os.path.exists(tar_path):
        logger.error(f"TAR file does not exist: {tar_path}")
        return ""

    # Derive target folder name based on the tar file name
    submission_name = extract_submission_base_name(tar_path)
    dest_dir = os.path.join(destination_root, submission_name)
    os.makedirs(dest_dir, exist_ok=True)

    try:
        # Open and extract the contents of the tarball
        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(path=dest_dir)
        logger.info(f"Successfully unpacked {tar_path} to {dest_dir}")
        return dest_dir
    except Exception as e:
        logger.exception(f"Failed to unpack {tar_path}: {e}")
        return ""
