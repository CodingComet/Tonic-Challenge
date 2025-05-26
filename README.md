# Tonic Data Engineering Challenge

Run Instructions:
.env file:
JIRA_SERVER
EMAIL
API_TOKEN
PROJECT_KEY

### playground.py
Generates random issues with predefined server list.

### main.py
Fetches and performs analysis.

### example config.py
- PREDEFINED_SERVERS = ["srv-a", "srv-1", "srv-database3", "srv-00623"]

For main.py
- PROGRESS_FILE = "sync_checkpoint.json"
- PAGE_SIZE = 8

For playground.py
- TEMPLATES = [
    "We're seeing latency issues on {}.",
    "Disk space running low on {}.",
    "{} is crashing intermittently.",
    "Multiple issues reported with {}.",
    "Error logs found on {}.",
    "{} might be down.",
    "Users are reporting issues, possibly due to {}.",
    "Unexpected behavior observed (no server mentioned).",
    "Backup failed; might be related to {}.",
    "System rebooted. No server ID noted.",
]

- PRIORITIES = ["Low", "Medium", "High", "Critical"]
- PRIORITY_WEIGHTS = [0.4, 0.3, 0.2, 0.1]