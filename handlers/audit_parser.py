import os
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple

def parse_audit_xml(audit_path: str) -> Tuple[str, str, str, List[Dict[str, str]]]:
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
