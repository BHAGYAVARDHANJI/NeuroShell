# config.py

# AI Models
CLOUD_MODEL = "gemini-2.5-flash"
LOCAL_MODEL = "llama3"

# System Limits
LARGE_FILE_BYTES = 50 * 1024 * 1024  # 50 MB

# Directory Exclusions
IGNORE_DIRS = [
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    ".idea",
    ".vscode"
]

JUNK_DIRS = [
    "__pycache__",
    ".pytest_cache",
    "build",
    "dist"
]