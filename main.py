# main.py
import os
import subprocess
from rich.console import Console

# Agent Handlers
from agent.agent_brain import organize_project
from agent.cleanup_agent import plan_cleanup, execute_cleanup
from agent.disk_scanner import scan_disk
from agent.planner_agent import plan_task
from agent.project_analyzer import collect_project_files
from agent.agent_loop import run_agent

# Core Systems
from core.ai_engine import hybrid_ai_router, analyze_project
from core.intent_detector import detect_intent
from core.memory_engine import suggest, get_command, learn_command
from core.security_validator import analyze_command

console = Console()

# ==========================================
# COMMAND HANDLERS
# ==========================================

def handle_analyze_project(user_input):
    console.print("Scanning project...", style="cyan")
    files = collect_project_files(".")
    console.print("Sending to AI...", style="cyan")
    report = analyze_project(files)
    console.print("\nAI Project Report:\n", style="bold green")
    console.print(report)

def handle_scan_disk(user_input):
    parts = user_input.split()
    path = parts[2] if len(parts) > 2 else "."
    console.print(f"\nScanning: {path}", style="bold cyan")
    results = scan_disk(path)
    console.print("\nLargest Files:", style="bold cyan")
    for size, file in results:
        console.print(f"{size / 1024 / 1024:.2f} MB -> {file}")

def handle_organize_project(user_input):
    console.print("Agent analyzing project...", style="cyan")
    actions = organize_project()
    console.print("\nAgent Suggestions:", style="bold green")
    for act in actions:
        console.print(f"- {act}")

def handle_clean_project(user_input):
    console.print("Agent planning cleanup...", style="cyan")
    actions = plan_cleanup()
    if not actions:
        console.print("No junk folders found.", style="green")
        return
    console.print("\nCleanup Plan:", style="bold yellow")
    for action in actions:
        console.print(f"- Delete -> {action}")
    confirm = input("Execute cleanup? (y/n): ")
    if confirm.lower() == "y":
        execute_cleanup(actions)
        console.print("Cleanup completed.", style="bold green")

def handle_optimize_project(user_input):
    console.print("Agent planning optimization...", style="cyan")
    plan = plan_task(user_input)
    if not plan:
        console.print("No optimization needed.", style="green")
        return
    console.print("\nOptimization Plan:", style="bold yellow")
    for step in plan:
        console.print(f"- {step[1]}")
    confirm = input("Execute plan? (y/n): ")
    if confirm.lower() == "y":
        for step in plan:
            if step[0] == "cleanup":
                actions = plan_cleanup()
                execute_cleanup(actions)
            elif step[0] == "structure":
                os.makedirs("logs", exist_ok=True)
                console.print("[OK] logs folder created")
            elif step[0] == "report":
                console.print("[OK] Optimization complete")

def handle_run_agent(user_input):
    goal = user_input.replace("agent ", "", 1)
    run_agent(goal)

# ==========================================
# SYSTEM EXECUTION & REGISTRY
# ==========================================

def execute_system_command(command, original_input, from_memory=False):
    risk = analyze_command(command)
    if risk == "HIGH":
        console.print("HIGH RISK command blocked!", style="bold red")
        return

    console.print(f"Risk Level: {risk}", style="cyan")
    confirm = input("Execute? (y/n): ").lower()

    if confirm == "y":
        if risk == "SAFE":
            subprocess.run(command, shell=True)
            if not from_memory:
                learn_command(original_input, command)
        else:
            console.print(f"[SAFE MODE] Would execute: {command}", style="yellow")

def handle_general_ai(user_input, intent):
    remembered = get_command(user_input)
    if remembered:
        console.print(f"[Memory] AI Response: {remembered}", style="green")
        execute_system_command(remembered, user_input, from_memory=True)
        return

    ai_output = hybrid_ai_router(user_input, intent)
    console.print(f"AI Response: {ai_output}", style="yellow")

    if intent == "general_question":
        return

    if "[" in ai_output and "Error" in ai_output:
        console.print("AI failed to generate valid command.", style="red")
        return

    execute_system_command(ai_output, user_input)

# The Command Registry maps intents to their specific functions
COMMAND_REGISTRY = {
    "analyze_project": handle_analyze_project,
    "scan_disk": handle_scan_disk,
    "organize_project": handle_organize_project,
    "clean_project": handle_clean_project,
    "optimize_project": handle_optimize_project,
    "run_agent": handle_run_agent
}

def main():
    console.print("Welcome to NeuroShell AI Terminal", style="bold green")

    while True:
        user_input = input("NeuroShell > ").strip()
        if not user_input:
            continue

        # Interactive Autocomplete
        suggestions = suggest(user_input)
        if suggestions:
            best = suggestions[0]
            if user_input.lower() != best and len(user_input) < len(best):
                console.print(f"Did you mean -> {best} ? (y/n)", style="dim")
                if input().lower() == 'y':
                    user_input = best

        intent = detect_intent(user_input)

        if intent == "exit":
            console.print("Exiting NeuroShell...", style="bold red")
            break

        # Route the command using the Registry
        if intent in COMMAND_REGISTRY:
            handler = COMMAND_REGISTRY[intent]
            handler(user_input)
        else:
            handle_general_ai(user_input, intent)

if __name__ == "__main__":
    main()