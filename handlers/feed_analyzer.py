import os
import glob
import xml.etree.ElementTree as ET
from audit_parser import parse_audit_xml
from services.auto_fixer import fix_submission
from services.schema_validator import load_schema, validate_data_against_schema
from utils.logger import get_logger
from utils.grafana_logger import log_event

logger = get_logger()

AUTO_FIX_ENABLED = True

def analyze_feed(submission_path: str) -> bool:
    base_name = os.path.basename(submission_path)
    log_path = os.path.join(submission_path, "feed_analysis.log")
    issues = []

    REQUIRED_EXTENSIONS = [".audit.xml", ".control"]
    for ext in REQUIRED_EXTENSIONS:
        pattern = os.path.join(submission_path, f"{base_name}{ext}")
        if not glob.glob(pattern):
            issues.append(f"Missing required file with extension '{ext}' matching base name.")

    data_files = glob.glob(os.path.join(submission_path, f"{base_name}.U*.data"))
    if not data_files:
        issues.append("No data files (.U*.data) found.")

    control_path = os.path.join(submission_path, f"{base_name}.control")
    if os.path.exists(control_path) and os.path.getsize(control_path) != 0:
        issues.append(f"Control file '{control_path}' must be exactly 0 bytes.")

    audit_path = os.path.join(submission_path, f"{base_name}.audit.xml")
    if os.path.exists(audit_path):
        try:
            ET.parse(audit_path)
        except ET.ParseError:
            issues.append(f"Audit XML '{audit_path}' is not well-formed.")

    if os.path.exists(audit_path) and not issues:
        try:
            _, _, _, audit_files = parse_audit_xml(audit_path)
            for item in audit_files:
                expected_path = os.path.join(submission_path, item["file_name"])
                if not os.path.exists(expected_path):
                    issues.append(f"File listed in audit.xml not found: {item['file_name']}")
                else:
                    with open(expected_path, "r", encoding="utf-8") as f:
                        line_count = sum(1 for _ in f) - 1
                        if line_count != item["record_count"]:
                            issues.append(f"Record count mismatch in {item['file_name']}: expected {item['record_count']}, found {line_count}")
        except Exception as e:
            issues.append(f"Error parsing audit.xml contents: {e}")

    # Validate schema if present
    schema_path = os.path.join(submission_path, "schema.txt")
    if os.path.exists(schema_path):
        try:
            schema = load_schema(schema_path)
            for data_file in data_files:
                validation_errors = validate_data_against_schema(data_file, schema)
                issues.extend(validation_errors)
        except Exception as e:
            issues.append(f"Error validating schema: {e}")
    else:
        issues.append("schema.txt not found in submission.")

    if issues and AUTO_FIX_ENABLED:
        fixed = fix_submission(submission_path, base_name)
        if fixed:
            logger.info(f"[{base_name}] Auto-fix applied. Retrying validation...")
            return analyze_feed(submission_path)

    with open(log_path, "w") as log_file:
        if not issues:
            log_file.write("Validation PASSED.\n")
            logger.info(f"[{base_name}] Validation PASSED.")
            log_event("validation_passed", base_name, "structure_check", "All checks passed")
            return True
        else:
            log_file.write("Validation FAILED:\n")
            for issue in issues:
                log_file.write(f"- {issue}\n")
                logger.warning(f"[{base_name}] {issue}")
            log_event(
                event="validation_failed",
                submission=base_name,
                event_type="schema_validation",
                detail=f"{len(issues)} issues found: " + "; ".join(issues[:3]),
                critical=True,
                recommended_action="Check feed_analysis.log in rejected folder for full list of errors."
            )
            return False
