import os

SYSTEM_PATHS = [
    "c:\\",
    "c:/",
    "windows",
    "system32",
    "program files"
]

DANGEROUS_KEYWORDS = [
    "format",
    "shutdown",
    "rmdir",
    "del",
    "remove-item",
    "rd",
    "rm"
]

def analyze_command(command):

    cmd = command.lower()

    # HIGH RISK → system paths
    for path in SYSTEM_PATHS:
        if path in cmd:
            return "HIGH"

    # MEDIUM RISK → destructive keywords
    for key in DANGEROUS_KEYWORDS:
        if key in cmd:
            return "MEDIUM"

    return "SAFE"