"""
grafana_logger.py

Provides a structured logging utility that emits events in JSONL format,
ready to be picked up by Grafana, Loki, FluentBit, or any structured log collector.

Each line represents a single event. These logs can be used for monitoring feed
validation status and triggering alerts/tickets (e.g., in ServiceNow).
"""

import os
import json
from datetime import datetime
from typing import Optional

# Path to JSONL log file for Grafana ingestion
GRAFANA_LOG_PATH = "./logs/grafana_feed_events.jsonl"

def log_event(
    event: str,
    submission: str,
    event_type: str,
    detail: str,
    critical: bool = False,
    recommended_action: Optional[str] = None,
    contact: Optional[str] = "datafeeds-support@example.com",
    source_system: str = "HDR LZ Validator"
):
    """
    Logs a structured event in JSONL format for observability.

    Args:
        event: Event name (e.g. validation_failed, validation_passed)
        submission: Submission identifier
        event_type: Category/type of the event
        detail: Short description or summary
        critical: Whether the event is considered high priority
        recommended_action: Optional suggestion for feed sender
        contact: Email or team responsible for support
        source_system: Name of the system emitting the event
    """
    log_entry = {
        "event": event,
        "submission": submission,
        "type": event_type,
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "critical": critical,
        "recommended_action": recommended_action,
        "source_system": source_system,
        "contact": contact
    }

    os.makedirs(os.path.dirname(GRAFANA_LOG_PATH), exist_ok=True)
    with open(GRAFANA_LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
