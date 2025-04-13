import os
import json
from datetime import datetime
from typing import Optional

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
