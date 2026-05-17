from agent.dependency_agent import check_dependencies
import json
from rich.console import Console

from core.ai_engine import local_agent_reasoning
from agent.project_analyzer import collect_project_files
from agent.cleanup_agent import plan_cleanup, execute_cleanup
from agent.agent_brain import organize_project
from agent.planner_agent import plan_task
from agent.git_agent import get_git_status, commit_changes, init_git

console = Console()

def run_agent(goal):
    console.print(f"\n[bold magenta]🧠 NeuroShell Agent Mode Started[/bold magenta]")
    console.print(f"🎯 Goal: {goal}\n")

    actions_taken = []
    last_result = "None"

    for step in range(8):  # Increased steps for complex tasks
        console.print(f"\n[bold blue]----- Agent Thinking Step {step+1} -----[/bold blue]")

        prompt = f"""
You are NeuroShell, an Autonomous Terminal Agent.
GOAL: {goal}
PREVIOUS ACTIONS: {actions_taken}
LAST RESULT: {last_result}

AVAILABLE TOOLS:
- analyze_project: Scans the codebase for architecture and bugs.
- cleanup_project: Finds and deletes junk/cache folders.
- organize_project: Suggests organization for files/folders.
- optimize_project: Creates a task optimization plan.
- check_git_status: Checks if there are uncommitted changes.
- init_git: Initializes a new empty Git repository.
- commit_code: Commits all changes. REQUIRES a "parameter" field with the commit message.
- check_dependencies: Scans the project for missing Python packages.
- finish: Use this when the goal is completely achieved.

RULES:
- You must respond in STRICT JSON format.
- Do not include any markdown formatting, backticks, or extra text.
- Do not repeat the same action if it failed.
- CRITICAL: Once the specific tasks requested in the GOAL are completed, you MUST choose the 'finish' action immediately.

EXPECTED JSON FORMAT:
{{
    "thought": "Brief explanation of what to do next and why",
    "action": "tool_name_from_list",
    "parameter": "Optional string, use only if the tool requires it (like a commit message)"
}}
"""
        response = local_agent_reasoning(prompt)

        try:
            clean_json = response.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:-3].strip()
            elif clean_json.startswith("```"):
                clean_json = clean_json[3:-3].strip()

            parsed_response = json.loads(clean_json)
            thought = parsed_response.get("thought", "Thinking...")
            action = parsed_response.get("action", "").lower()
            parameter = parsed_response.get("parameter", "")

            console.print(f"[cyan]Agent Thought:[/cyan] {thought}")

        except json.JSONDecodeError:
            console.print("[red]Agent got confused and returned invalid format. Retrying...[/red]")
            last_result = "Error: Invalid JSON format. Try again using strictly the requested JSON format."
            continue

        if len(actions_taken) >= 2 and actions_taken[-1] == action and actions_taken[-2] == action:
            console.print("[yellow][Agent] Repeated action detected. Forcing finish to prevent infinite loop.[/yellow]")
            action = "finish"

        actions_taken.append(action)

        # =========================
        # TOOL EXECUTION
        # =========================
        if action == "analyze_project":
            files = collect_project_files(".")
            last_result = f"Project has {len(files)} files scanned."
            console.print(f"[green]✔ Action Executed:[/green] {last_result}")

        elif action == "cleanup_project":
            actions = plan_cleanup()
            if actions:
                execute_cleanup(actions)
                last_result = f"Cleaned {len(actions)} junk items."
            else:
                last_result = "No junk folders found to clean."
            console.print(f"[green]✔ Action Executed:[/green] {last_result}")

        elif action == "organize_project":
            suggestions = organize_project()
            last_result = f"Found {len(suggestions)} organization suggestions."
            console.print("[green]✔ Action Executed:[/green] Generated suggestions.")

        elif action == "optimize_project":
            plan = plan_task(goal)
            if plan:
                last_result = f"Generated optimization plan with {len(plan)} steps."
                console.print("[green]✔ Action Executed:[/green] Optimization Plan generated.")
            else:
                last_result = "No optimization needed."
                console.print(f"[green]✔ Action Executed:[/green] {last_result}")

        elif action == "init_git":
            last_result = init_git()
            console.print(f"[green]✔ Action Executed:[/green] {last_result}")

        elif action == "check_git_status":
            last_result = get_git_status()
            console.print(f"[green]✔ Action Executed:[/green]\n{last_result}")

        elif action == "check_dependencies":
            last_result = check_dependencies()
            console.print(f"[green]✔ Action Executed:[/green]\n{last_result}")
        
        elif action == "commit_code":
            msg = parameter if parameter else "Auto-commit by NeuroShell"
            last_result = commit_changes(msg)
            console.print(f"[green]✔ Action Executed:[/green] {last_result}")
            
            # Force the agent to finish if the commit was successful
            if "Successfully committed" in last_result:
                console.print("\n[bold green]✅ Goal achieved. Forcing agent to finish.[/bold green]")
                break
            
        elif action == "finish":
            console.print("\n[bold green]✅ Agent has successfully completed the goal.[/bold green]")
            break

        else:
            last_result = f"Error: Tool '{action}' does not exist."
            console.print(f"[red]✖ Unknown action: {action}[/red]")