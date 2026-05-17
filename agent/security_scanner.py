# agent/security_scanner.py
import os
import re
from core.config import IGNORE_DIRS

# Regex patterns for finding exposed secrets
DANGEROUS_PATTERNS = {
    "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Generic Secret": r"(?i)(secret|password|token|api_key|apikey)[\s:=]+['\"][^\s]+['\"]"
}

def scan_for_secrets():
    """Scans the project files for exposed API keys and secrets."""
    report = []
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d.lower() not in IGNORE_DIRS]
        
        for file in files:
            if file.endswith(('.exe', '.dll', '.so', '.pyc', 'package-lock.json', '.png', '.jpg')):
                continue
                
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines):
                    # Flag anything that matches our dangerous patterns
                    for key_type, pattern in DANGEROUS_PATTERNS.items():
                        if re.search(pattern, line):
                            # Ignore the config and .env files themselves to prevent false positives during normal operation
                            if "config.py" not in full_path and ".env" not in full_path:
                                report.append(f"🚨 [WARNING] {key_type} found in {full_path} (Line {line_num + 1})")
            except Exception:
                pass
                
    if not report:
        return "✅ Security Scan Passed: No exposed secrets found."
        
    return "\n".join(report)