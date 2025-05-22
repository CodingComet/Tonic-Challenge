from jira import JIRA
import time
import os
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

import signal
import sys
import json

terminate_requested = False


def handle_termination(signum, frame):
    global terminate_requested
    print(
        f"\n[!] Termination requested (signal {signum}) — stopping after current batch..."
    )
    terminate_requested = True


# Register signal handlers
signal.signal(signal.SIGINT, handle_termination)  # Ctrl+C
signal.signal(signal.SIGTERM, handle_termination)  # kill


PROGRESS_FILE = "sync_checkpoint.json"


def load_checkpoint():
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[!] Didn't load checkpoint: {e}")
    return []


def save_checkpoint(descriptions):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(descriptions, f)


# === CONFIGURATION ===
load_dotenv()

JIRA_SERVER = os.getenv("JIRA_SERVER")
EMAIL = os.getenv("EMAIL")
API_TOKEN = os.getenv("API_TOKEN")
PROJECT_KEY = os.getenv("PROJECT_KEY")

# === CONNECT TO JIRA ===
jira = JIRA(server=JIRA_SERVER, basic_auth=(EMAIL, API_TOKEN))


def fetch_issues(start_at: int, max_results: int):
    issues = jira.search_issues(
        f"project={PROJECT_KEY}",  # JQL query to filter by project
        fields="description",
        startAt=start_at,
        maxResults=max_results,
    )
    return issues


def fetch_all_issues(max_results: int = 8):
    all_descriptions = load_checkpoint()
    if all_descriptions == []:
        start_at = 0
    else:
        start_at = len(all_descriptions)

    while True:
        if terminate_requested:
            save_checkpoint(all_descriptions)

            sys.exit()

        last_issues = fetch_issues(start_at, max_results)
        if not last_issues:
            break
        
        all_descriptions += [issue.fields.description for issue in last_issues]
        start_at += max_results
    return all_descriptions


def count_server_occurences(servers: list[str]):
    all_descriptions = fetch_all_issues(50)

    no_associated_servers = 0
    occurences = np.zeros(len(servers))

    for description in all_descriptions:
        lower = description.lower()
        associated = np.array(
            [lower.count(server_name) for server_name in server_names]
        )
        if np.all(associated == 0):
            no_associated_servers += 1
        else:
            occurences += associated
    return no_associated_servers, occurences


def render_results():
    server_names = ["srv-a", "srv-1", "srv-database3", "srv-00623"]
    no_server_mentioned, occurences = count_server_occurences(server_names)


    all_titles = np.append(server_names, "NO SERVER MENTIONED")
    all_amounts = np.append(occurences, no_server_mentioned)

    # Bar colors: blue for existing, red for extra
    colors = ["blue"] * len(occurences) + ["red"]

    # Plotting
    plt.bar(all_titles, all_amounts, color=colors)
    plt.ylabel("#")
    plt.title("Mentions of Each Server")
    plt.show()

if __name__ == "__main__":
    render_results()
