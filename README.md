# Landing Zone Feed Validator

This Python-based application validates feed submission packages (`.tar`) intended for HDR/TransArch systems. It unpacks, validates structure and content, auto-fixes minor issues, and prepares feed packages for further transfer (e.g., via MFT). Validation results are logged both as human-readable logs and structured JSONL logs for Grafana/ServiceNow integration.

## 🔧 What it does

1. Scans the `incoming/` folder for `.tar` files  
2. Unpacks each `.tar` into `workspace/`  
3. Validates:
   - Required files are present (e.g., `.audit.xml`, `.control`, `.U*.data`)
   - Filenames follow expected naming conventions
   - `audit.xml` matches files and record counts
   - `schema.txt` (if present) matches the structure of `.data` files  
4. Applies basic auto-fixes:
   - Resets `.control` file to 0 bytes if needed
   - Adds header to `.data` file if missing  
5. On success → moves feed to `ready_for_mft/`  
6. On failure → moves feed to `rejected/` and logs details  

## 📁 Folder Structure

- `incoming/` – Drop your `.tar` files here  
- `workspace/` – Temporary unpacking area  
- `ready_for_mft/` – Feeds that passed validation and are ready for transfer  
- `rejected/` – Feeds that failed validation  
- `logs/` – System logs (`app.log`) and Grafana logs (`grafana_feed_events.jsonl`)  

## ▶️ How to run

Make sure Python 3 is installed. Then from the project directory:

```
python main.py
```

The app will automatically process all `.tar` files in the `incoming/` folder.

## 📆 What goes into a `.tar` feed

A valid `.tar` feed should contain:
- `*.audit.xml` – Submission metadata  
- `*.control` – Empty control file (must be 0 bytes)  
- `*.U*.data` – One or more CSV files with headers  
- `schema.txt` – (Optional) JSON schema describing column structure  

## ✅ Example `schema.txt`

```
[
  {"name": "ID", "nullable": false, "type": "long"},
  {"name": "AMOUNT", "nullable": false, "type": "decimal"},
  {"name": "REGION", "nullable": true, "type": "string"}
]
```

## 🧐 Auto-fix capabilities

If `AUTO_FIX_ENABLED = True`, the system may attempt:
- Resetting `.control` file size to 0 bytes  
- Inserting missing headers into `.data` files  

All auto-fix actions are logged and can be extended in `auto_fixer.py`.

## 📊 Grafana / ServiceNow integration

- High-level events are logged in `logs/grafana_feed_events.jsonl` (JSON Lines format)
- Log structure is compatible with ingestion by Grafana/Loki or Logstash
- Alerts can be configured to generate ServiceNow (GSnow) tickets based on validation failures
- Each log includes recommended corrective actions for feed owners

## 📬 Contact

For support or onboarding:  
**datafeeds-support@example.com**

