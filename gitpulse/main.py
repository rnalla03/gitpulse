from datetime import datetime, timedelta
from git import Repo
from git.exc import InvalidGitRepositoryError
from rich.console import Console
from collections import Counter
import os
import sys
import requests

console = Console()

# ------------------------------
# Local Repo Commit Analysis
# ------------------------------
def get_local_commit_counts(repo_path, days=7):
    repo_path = os.path.abspath(os.path.expanduser(repo_path))

    try:
        repo = Repo(repo_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        console.print(f"[red]Error:[/] '{repo_path}' is not a valid Git repository.")
        sys.exit(1)

    now = datetime.now()
    since_date = now - timedelta(days=days)

    commits = list(repo.iter_commits(since=since_date.isoformat()))
    days_list = [datetime.fromtimestamp(c.committed_date).strftime("%a") for c in commits]
    counts = Counter(days_list)

    all_days = [(now - timedelta(days=i)).strftime("%a") for i in range(days - 1, -1, -1)]
    data = [(day, counts.get(day, 0)) for day in all_days]
    return data


# ------------------------------
# Remote GitHub Repo Commit Analysis
# ------------------------------
def get_remote_commit_counts(repo_full_name, days=7):
    now = datetime.utcnow()
    since_date = (now - timedelta(days=days)).isoformat() + "Z"

    url = f"https://api.github.com/repos/{repo_full_name}/commits"
    params = {"since": since_date, "per_page": 100}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        console.print(f"[red]Error:[/] Unable to fetch from GitHub API "
                      f"({response.status_code}). Make sure the repo is public.")
        sys.exit(1)

    commits = response.json()
    days_list = [
        datetime.fromisoformat(c["commit"]["author"]["date"].replace("Z", "")).strftime("%a")
        for c in commits if "commit" in c and "author" in c["commit"]
    ]

    counts = Counter(days_list)
    all_days = [(now - timedelta(days=i)).strftime("%a") for i in range(days - 1, -1, -1)]
    data = [(day, counts.get(day, 0)) for day in all_days]
    return data


# ------------------------------
# Shared Chart Printing
# ------------------------------
def print_commit_chart(data, title="📈 GitPulse: Commit Activity (Last 7 Days)"):
    console.rule(f"[bold blue]{title}")

    max_count = max((count for _, count in data), default=1)
    total_commits = sum(count for _, count in data)
    most_active_day, most_active_count = max(data, key=lambda x: x[1])

    for day, count in data:
        if count == 0:
            bar = "░"
            color = "grey50"
        else:
            bar_len = int((count / max_count) * 20)
            bar = "█" * bar_len
            color = "green" if count < 5 else "yellow" if count < 10 else "red"

        console.print(f"{day:>3} | [{color}]{bar:<20}[/{color}] {count}")

    console.rule(f"[bold green]✅ Total Commits:[/] {total_commits} | "
                 f"[cyan]Most Active:[/] {most_active_day} ({most_active_count} commits)")
    console.rule("[dim]End of report")


# ------------------------------
# CLI Entry Point
# ------------------------------
def main():
    args = sys.argv[1:]

    # Default behavior → analyze local repo
    if not args:
        repo_path = os.getcwd()
        data = get_local_commit_counts(repo_path)
        print_commit_chart(data)
        return

    # Check for remote mode
    if "--remote" in args:
        try:
            repo_full_name = args[args.index("--remote") + 1]
        except IndexError:
            console.print("[red]Error:[/] Please provide a GitHub repo name. Example: --remote vercel/next.js")
            sys.exit(1)

        data = get_remote_commit_counts(repo_full_name)
        print_commit_chart(data, title=f"🌐 GitPulse: Remote Repo Activity ({repo_full_name})")
    else:
        # Local mode with explicit path
        repo_path = args[0]
        data = get_local_commit_counts(repo_path)
        print_commit_chart(data)
