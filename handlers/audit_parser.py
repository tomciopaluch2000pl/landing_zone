"""
audit_parser.py

Parses the .audit.xml file in a feed submission.
Extracts the base name, sequence number, version, and expected files with record counts.
Used during validation to verify audit metadata vs. actual file presence and size.
"""

import os
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

def parse_audit_xml(audit_path: str) -> Tuple[str, str, str, List[Dict[str, str]]]:
    """
    Parses the audit.xml file and extracts submission metadata and file info.

    Args:
        audit_path: Path to the .audit.xml file

    Returns:
        Tuple of:
            - base name (str)
            - sequence number (str)
            - version (str)
            - list of file info dictionaries, each with:
                * file_name (str)
                * record_count (int)

    Raises:
        FileNotFoundError: If audit.xml file does not exist
        ET.ParseError: If XML is malformed
    """
    if not os.path.exists(audit_path):
        raise FileNotFoundError(f"Audit XML file not found: {audit_path}")

    tree = ET.parse(audit_path)
    root = tree.getroot()

    submission_base_name = root.findtext("SubmissionBaseName", default="")
    sequence_number = root.findtext("SubmissionSequenceNumber", default="")
    version = root.findtext("SubmissionVersion", default="")

    file_info_list = []
    for file_elem in root.findall(".//File"):
        file_name = file_elem.findtext("FileName", default="")
        record_count = file_elem.findtext("RecordCount", default="0")
        file_info_list.append({
            "file_name": file_name.strip(),
            "record_count": int(record_count)
        })

    return submission_base_name, sequence_number, version, file_info_list
