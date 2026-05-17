# core/intent_detector.py

def detect_intent(query):
    query = query.lower().strip()

    # Detect built-in NeuroShell tools
    if "analyze this project" in query:
        return "analyze_project"
    if query.startswith("scan disk"):
        return "scan_disk"
    if "organize project" in query:
        return "organize_project"
    if "clean project" in query:
        return "clean_project"
    if "optimize project" in query:
        return "optimize_project"
    if query.startswith("agent "):
        return "run_agent"
    if query == "exit":
        return "exit"

    # Fallback to general AI classification (Expanded for Linux)
    command_words = [
        "list", "create", "delete", "remove", 
        "scan", "cd", "dir", "mkdir", "file", "folder",
        "update", "upgrade", "download", "install",
        "get", "fetch", "run", "execute", "start", "stop",
        "apt", "pacman", "dnf", "wget", "curl", "git"
    ]

    for word in command_words:
        if word in query:
            return "general_command"

    return "general_question"