# agent/dependency_agent.py
import os
import ast
import sys

def check_dependencies():
    """Scans Python files for imports and checks if they are installed."""
    
    # Get standard Python libraries so we don't try to pip install 'os' or 'sys'
    stdlib = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set(sys.builtin_module_names)
    
    # Map import names to their actual pip package names
    pkg_map = {
        "dotenv": "python-dotenv",
        "google": "google-generativeai",
        "genai": "google-genai",
        "cv2": "opencv-python",
        "bs4": "beautifulsoup4"
    }

    imports = set()
    
    # 1. Scan the project for all imported modules
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ["venv", "__pycache__", ".git"]]
        for file in files:
            if file.endswith(".py"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom) and node.module:
                                imports.add(node.module.split('.')[0])
                except Exception:
                    pass

    missing = []
    
    # 2. Test if the found modules are actually installed
    for mod in imports:
        # Ignore standard library and local files
        if mod in stdlib or os.path.exists(f"{mod}.py") or os.path.exists(f"{mod}/__init__.py"):
            continue
        
        try:
            __import__(mod)
        except ImportError:
            # If it fails to import, figure out the right pip command
            pip_name = pkg_map.get(mod, mod)
            missing.append(pip_name)

    # 3. Report the findings
    if not missing:
        return "✅ All project dependencies are correctly installed."
        
    packages = " ".join(set(missing))
    return f"🚨 Missing Dependencies Detected!\nRun this command to fix: pip install {packages}"