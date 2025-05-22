from jira import JIRA
import time
import dotenv
import os

from dotenv import load_dotenv

# === CONFIGURATION ===
load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# === CONNECT TO JIRA ===
jira = JIRA(server=JIRA_SERVER, basic_auth=(EMAIL, API_TOKEN))

issue_dict = {
    "project": {"key": PROJECT_KEY},
    "summary": f"TEST SINGLE ISSUE",
    "issuetype": {"name": "Task"},
}
try:
    issue = jira.create_issue(fields=issue_dict)
    print(f"Created: {issue.key}")
except Exception as e:
    print(f"Failed to create issue: {e}")
