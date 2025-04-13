# Developer README – Landing Zone Feed Validator

This document provides developer-level guidance for understanding, extending, and maintaining the Landing Zone Feed Validator. The system processes `.tar` submissions for HDR/TransArch, validates them, auto-fixes common errors, and logs results for monitoring and integration.

---

## ⚙️ Project Structure

```
landingzone_app/
├── main.py                     # Entry point for processing all .tar files
├── config/
│   └── settings.yaml           # Placeholder for configuration (future use)
├── handlers/
│   ├── feed_analyzer.py        # Performs validation logic on unpacked feed
│   ├── unpacker.py             # Extracts submission .tar into workspace/
│   └── audit_parser.py         # Parses .audit.xml and extracts metadata
├── services/
│   ├── auto_fixer.py           # Automatically fixes known validation issues
│   ├── schema_validator.py     # Validates data files against schema.txt
│   └── mft_sender.py           # Simulates MFT transfer (stub)
├── utils/
│   ├── logger.py               # Configures console + file logging
│   └── grafana_logger.py       # Outputs JSONL log events for Grafana/GSnow
├── workspace/                  # Temp folder for unpacked submissions
├── incoming/                   # Drop .tar files here for processing
├── rejected/                   # Submissions with validation errors
├── ready_for_mft/              # Successfully validated submissions
├── logs/
│   ├── app.log                 # Human-readable system log
│   └── grafana_feed_events.jsonl  # Structured JSON log
├── requirements.txt            # Python dependencies (empty for now)
└── .gitignore
```

---

## 🧠 Core Workflow (main.py)

1. Scan `incoming/` for `.tar` files
2. Unpack each file to `workspace/`
3. Validate feed using `feed_analyzer.py`
4. If valid → move to `ready_for_mft/` and call MFT stub
5. If invalid → move to `rejected/` and log errors
6. Log all steps to both app.log and JSONL for Grafana

---

## 🔍 Validation Logic (feed_analyzer.py)

- Required files:
  - `*.audit.xml` (must be well-formed)
  - `*.control` (must be 0 bytes)
  - `*.U*.data` (CSV with headers)
  - `schema.txt` (optional but recommended)

- Audit consistency checked via `audit_parser.py`
- Schema validated via `schema_validator.py`
- Errors logged in `feed_analysis.log` + `grafana_feed_events.jsonl`
- Auto-fix reattempts validation if enabled

---

## 🛠 Auto-Fix Logic (auto_fixer.py)

Fixes known minor problems:
- Control file not empty → resets to 0 bytes
- Missing CSV headers → inserts generic header (`COL1;COL2;...`)

More fix strategies can be added easily in `fix_submission()`

---

## 📡 Integration Support

- All events are logged as JSON Lines in `logs/grafana_feed_events.jsonl`
- Format is suitable for:
  - Grafana Loki
  - Fluent Bit
  - Logstash → Elasticsearch
- Tickets can be created in GSnow (ServiceNow) via alert rules

Example JSONL log:
```json
{
  "event": "validation_failed",
  "submission": "hd0000001.20240101.S001.V1",
  "type": "schema_validation",
  "detail": "Header column mismatch",
  "timestamp": "2025-04-14T08:33:22Z",
  "critical": true,
  "recommended_action": "Fix column names in data file.",
  "source_system": "HDR LZ Validator",
  "contact": "datafeeds-support@example.com"
}
```

---

## ✅ Developer Notes

- Python 3.x required
- No external packages used (pure standard library)
- All core logic lives in `handlers/` and `services/`
- Set `AUTO_FIX_ENABLED = True` in `feed_analyzer.py` to enable retry after fixes
- All `.py` files include clear headers and inline comments for clarity

---

## 📬 Support

Developer / Technical contact: `datafeeds-support@example.com`
