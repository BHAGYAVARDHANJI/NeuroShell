# agent/git_agent.py
import subprocess
from agent.security_scanner import scan_for_secrets

def init_git():
    """Initializes a new Git repository."""
    try:
        subprocess.run(["git", "init"], capture_output=True, check=True, text=True)
        return "Successfully initialized an empty Git repository."
    except subprocess.CalledProcessError as e:
        return f"Error: Failed to initialize Git repository. {e}"
    except FileNotFoundError:
        return "Error: Git is not installed on this system."

def get_git_status():
    """Returns the current status of the git repository."""
    try:
        result = subprocess.run(["git", "status", "-s"], capture_output=True, text=True, check=True)
        if not result.stdout.strip():
            return "Working directory is clean. Nothing to commit."
        return f"Uncommitted changes:\n{result.stdout.strip()}"
    except subprocess.CalledProcessError:
        return "Error: This directory is not a Git repository."
    except FileNotFoundError:
        return "Error: Git is not installed on this system."

def commit_changes(message):
    """Adds all changes and commits them, but ONLY if no secrets are found."""
    
    # 🚨 SECURITY CHECK: Run the scanner before doing anything
    security_report = scan_for_secrets()
    if "✅" not in security_report:
        return f"🚨 COMMIT BLOCKED! Exposed secrets found in your code:\n{security_report}\nFix these before committing."

    try:
        subprocess.run(["git", "status"], capture_output=True, check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        return f"Security Scan Passed. Successfully committed all changes with message: '{message}'"
    except subprocess.CalledProcessError:
        return "Error: Failed to commit. Make sure this is a Git repository and there are changes to commit."