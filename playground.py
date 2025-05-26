from jira import JIRA
import time
import dotenv
import os
import random
from config import *

from dotenv import load_dotenv

# === CONFIGURATION ===
load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# === CONNECT TO JIRA ===
jira = JIRA(server=JIRA_SERVER, basic_auth=(EMAIL, API_TOKEN))


def generate_description(servers: list[str], templates: list[str]):
    # Random number of servers: 0–3
    n_servers = random.choices([0, 1, 2, 3], weights=[0.1, 0.6, 0.2, 0.1])[0]
    chosen_servers = [
        s.upper() if random.random() > 0.5 else s
        for s in random.sample(servers, n_servers)
    ]

    if chosen_servers:
        s = ", ".join(chosen_servers)
        template = random.choice(templates[:-2])  # choose one that uses servers
        return template.format(s)
    else:
        return random.choice(templates[-2:])  # use no-server templates


def generate_random_issue(i: str, servers: list[str], templates: list[str]):
    priority = random.choices(PRIORITIES, weights=PRIORITY_WEIGHTS)[0]
    
    return {
        "project": {"key": PROJECT_KEY},
        "summary": f"ISSUE {i}",
        "description": generate_description(servers, templates),
        "issuetype": {"name": "Task"},
        "priority": {"name": priority},
    }



TOTAL_ISSUES = 50
ISSUES_IN_BATCH = 50
NUM_BATCHES = int(TOTAL_ISSUES / ISSUES_IN_BATCH)

for i in range(NUM_BATCHES):
    random_issues = [
        generate_random_issue(f"{i}.{j}", PREDEFINED_SERVERS, TEMPLATES)
        for j in range(ISSUES_IN_BATCH)
    ]
    try:
        issues = jira.create_issues(random_issues)
        
        print(f"Created: {issues[0]['issue'].key}...{issues[-1]['issue'].key}")
    except Exception as e:
        print(f"Failed to create issues: {e}")
