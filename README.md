#  GitPulse

**GitPulse** is a command-line tool that visualizes recent **Git commit activity** for both local repositories and public GitHub repositories.  




## Features
-  View commit activity from the **last 7 days**
- Works on **local repos** or **public GitHub repos**




##  Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/<your-username>/gitpulse.git
cd gitpulse
pip install -e .


After cloning and installing GitPulse, follow these steps to run the tool.

---

Option 1-
If you’re inside a git repo, simply run: gitpulse

Option 2-
You can provide the path to any local repository: gitpulse ~/Projects/my-repo

Option 3-
Analyze a public GitHub repository: gitpulse --remote vercel/next.js


Example Output: Remote Repo Activity (vercel/next.js)

Thu | ████░░░░░░░░░░░░░░░░░░ 5
Fri | ██░░░░░░░░░░░░░░░░░░░ 3
Mon | ███████████████████░░ 21
Tue | █████████████████████ 25
Wed | █████████████████░░░░ 19
Total Commits: 73 | Most Active: Tue (25 commits)
