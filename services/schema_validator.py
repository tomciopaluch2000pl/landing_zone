"""
schema_validator.py

Validates data files (.U*.data) against the column definitions specified in schema.txt.
The schema is a JSON file describing the column name, nullability, and data type.
Validation includes:
- Header name and count match
- Value type conformity
- Nullability enforcement

Used by the feed_analyzer to enforce schema correctness.
"""

import os
import json
from typing import List, Dict
from utils.logger import get_logger

# Initialize logger
logger = get_logger()

def load_schema(schema_path: str) -> List[Dict]:
    """
    Loads column definitions from a JSON schema file.

    Args:
        schema_path: Path to schema.txt (JSON)

    Returns:
        List of dictionaries with keys: name, nullable, type
    """
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_type(value: str, expected_type: str) -> bool:
    """
    Checks whether a given string value conforms to the expected data type.

    Args:
        value: The string value to check
        expected_type: One of: string, long, decimal, boolean, date

    Returns:
        True if value matches expected type, else False
    """
    if expected_type == "string":
        return True  # any string is valid
    elif expected_type == "long":
        return value.isdigit()
    elif expected_type == "decimal":
        try:
            float(value.replace(",", "."))  # supports comma as decimal
            return True
        except ValueError:
            return False
    elif expected_type == "boolean":
        return value.lower() in ["true", "false", "1", "0"]
    elif expected_type == "date":
        import re
        return bool(re.match(r"\d{4}-\d{2}-\d{2}", value))  # basic YYYY-MM-DD
    return False  # unknown type

def validate_data_against_schema(data_file: str, schema: List[Dict], delimiter: str = ";") -> List[str]:
    """
    Validates a .data file against a schema definition.

    Args:
        data_file: Path to the data file
        schema: Parsed schema definition
        delimiter: Column delimiter in the data file (default: ;)

    Returns:
        List of validation error messages
    """
    errors = []

    with open(data_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        errors.append(f"{data_file}: File is empty.")
        return errors

    headers = lines[0].strip().split(delimiter)

    # Check header count matches schema
    if len(headers) != len(schema):
        errors.append(f"{data_file}: Header column count does not match schema.")
        return errors

    # Check header names match schema
    for i, col_def in enumerate(schema):
        expected_name = col_def["name"]
        actual_name = headers[i].strip()
        if expected_name.upper() != actual_name.upper():
            errors.append(f"{data_file}: Column {i+1} mismatch: expected '{expected_name}', found '{actual_name}'.")

    # Check each row of data
    for line_no, line in enumerate(lines[1:], start=2):
        values = line.strip().split(delimiter)
        if len(values) != len(schema):
            errors.append(f"{data_file}, line {line_no}: Wrong number of values.")
            continue

        for i, value in enumerate(values):
            col_def = schema[i]
            value = value.strip('"')
            if not value and not col_def.get("nullable", True):
                errors.append(f"{data_file}, line {line_no}: Column {col_def['name']} is not nullable but is empty.")
            elif value and not validate_type(value, col_def["type"]):
                errors.append(f"{data_file}, line {line_no}: Value '{value}' in column {col_def['name']} does not match type '{col_def['type']}'.")

    return errors
