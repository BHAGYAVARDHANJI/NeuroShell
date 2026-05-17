import subprocess
import os
from google import genai

from dotenv import load_dotenv

load_dotenv(override=True)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# LOCAL COMMAND MODE
def local_ai(user_input):
    prompt = f"""
You are a Linux terminal expert.
Convert the user's instruction into an EXACT Linux bash command.
Output ONLY the raw command. 
Do NOT wrap it in backticks or markdown.
Do NOT explain the command.

Instruction: {user_input}
"""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    # Strip out any empty lines and grab the actual command
    lines = [line.strip() for line in result.stdout.split("\n") if line.strip()]
    return lines[-1] if lines else ""


# LOCAL REASONING MODE (fallback)
def local_reasoning(user_input):

    prompt = f"""
Answer in maximum 3 short lines.
Do not use bullet points.
Do not add headings.

Question: {user_input}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout.strip()

# LOCAL AGENT REASONING (For Agent Loop)
def local_agent_reasoning(prompt):

    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout.strip()


# CLOUD AI
def cloud_ai(user_input, intent="general_question"):
    print(">>> Trying CLOUD AI (Gemini)...")
    
    system_instruction = """
If the user asks for a command, download, or script, output ONLY the raw Linux bash command.
No markdown, no backticks, no explanations. 
If they ask a general question, answer normally but keep it brief.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_instruction}\n\nUser: {user_input}"
        )
        print(">>> CLOUD AI SUCCESS")
        
        clean_text = response.text.strip()
        if clean_text.startswith("```bash"):
            clean_text = clean_text[7:-3].strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:-3].strip()
            
        return clean_text

    except Exception as e:
        print(f">>> CLOUD AI FAILED: {e}")
        # ⭐ THE FIX: Route to the silent command generator if it's a command!
        if intent == "general_command":
            return local_ai(user_input)
        else:
            return local_reasoning(user_input)
        
def analyze_project(files):

    combined = ""

    for path, content in files:
        combined += f"\nFILE: {path}\n{content}\n"

    prompt = f"""
You are a senior software engineer.

Analyze this Python project and give:
- architecture feedback
- possible bugs
- improvement suggestions
- feature ideas

Project Files:
{combined}
"""

    return cloud_ai(prompt)
# ================= HYBRID ROUTER =================

def hybrid_ai_router(user_input, intent="general_question"):
    
    # Let the smart cloud try first for everything
    try:
        return cloud_ai(user_input, intent)
    except:
        # If offline, fall back based on intent
        if intent == "general_command":
            return local_ai(user_input)
        return local_reasoning(user_input)
    
    # ---- COMMAND TYPE ----
    for word in command_keywords:
        if user_input.lower().startswith(word):
            return local_ai(user_input)

    # ---- KNOWLEDGE TYPE ----
    for word in knowledge_keywords:
        if word in user_input.lower():
            return local_reasoning(user_input)

    # ---- COMPLEX → TRY CLOUD ----
    try:
        return cloud_ai(user_input)
    except:
        return local_reasoning(user_input)