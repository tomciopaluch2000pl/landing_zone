import os
import json
from typing import List, Dict
from utils.logger import get_logger

logger = get_logger()

def load_schema(schema_path: str) -> List[Dict]:
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_type(value: str, expected_type: str) -> bool:
    if expected_type == "string":
        return True
    elif expected_type == "long":
        return value.isdigit()
    elif expected_type == "decimal":
        try:
            float(value.replace(",", "."))
            return True
        except ValueError:
            return False
    elif expected_type == "boolean":
        return value.lower() in ["true", "false", "1", "0"]
    elif expected_type == "date":
        import re
        return bool(re.match(r"\d{4}-\d{2}-\d{2}", value))
    return False

def validate_data_against_schema(data_file: str, schema: List[Dict], delimiter: str = ";") -> List[str]:
    errors = []
    with open(data_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        errors.append(f"{data_file}: File is empty.")
        return errors

    headers = lines[0].strip().split(delimiter)
    if len(headers) != len(schema):
        errors.append(f"{data_file}: Header column count does not match schema.")
        return errors

    for i, col_def in enumerate(schema):
        expected_name = col_def["name"]
        actual_name = headers[i].strip()
        if expected_name.upper() != actual_name.upper():
            errors.append(f"{data_file}: Column {i+1} mismatch: expected '{expected_name}', found '{actual_name}'.")

    for line_no, line in enumerate(lines[1:], start=2):
        values = line.strip().split(delimiter)
        if len(values) != len(schema):
            errors.append(f"{data_file}, line {line_no}: Wrong number of values.")
            continue

        for i, value in enumerate(values):
            col_def = schema[i]
            if not value and not col_def.get("nullable", True):
                errors.append(f"{data_file}, line {line_no}: Column {col_def['name']} is not nullable but is empty.")
            elif value and not validate_type(value.strip('"'), col_def["type"]):
                errors.append(f"{data_file}, line {line_no}: Value '{value}' in column {col_def['name']} does not match type '{col_def['type']}'.")

    return errors
