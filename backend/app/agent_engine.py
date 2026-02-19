import os
import json
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# 1. ISOLATED WORKSPACE (Prevents reload issues)
BASE_TEMP_DIR = os.path.abspath("C:/rift-agent-workspace")
os.makedirs(BASE_TEMP_DIR, exist_ok=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)

# 2. MODEL CONFIG
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.1,
        "response_mime_type": "application/json"
    }
)

def get_agent_fix(error_log, code_context):
    """
    Mandatory Bug Types: LINTING, SYNTAX, LOGIC, TYPE_ERROR, IMPORT, INDENTATION
    """
    prompt = f"""
    SYSTEM: You are an Autonomous DevOps Agent fixing a CI/CD failure.
    
    TASK:
    1. Analyze the ERROR LOG to find the root cause.
    2. Classify as ONLY ONE: LINTING, SYNTAX, LOGIC, TYPE_ERROR, IMPORT, INDENTATION.
    3. Identify the EXACT line number in the provided code.
    4. Provide the FULL corrected content for the file.

    IMPORTANT: If the error is a logic bug, ensure the 'fixed_code' actually resolves the failure.

    ERROR LOG:
    {error_log}

    CURRENT CODE:
    {code_context}

    RETURN STRICTLY JSON:
    {{
      "bug_type": "TYPE",
      "explanation": "Short description of fix",
      "line_number": 0,
      "fixed_code": "full corrected file content"
    }}
    """
    try:
        response = model.generate_content(prompt)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("AI Fix Error:", e)
        return {
            "bug_type": "LOGIC",
            "explanation": "Fallback fix due to LLM error",
            "line_number": 0,
            "fixed_code": code_context
        }

def apply_patch(repo_path, relative_path, new_content):
    relative_path = relative_path.lstrip("/")
    full_path = os.path.join(repo_path, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def setup_repo_isolated(repo_url, team_name, leader_name):
    clean_team = team_name.upper().replace(" ", "_")
    clean_leader = leader_name.upper().replace(" ", "_")
    repo_path = os.path.join(BASE_TEMP_DIR, clean_team)

    if os.path.exists(repo_path):
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", repo_path], shell=True)

    subprocess.run(["git", "clone", repo_url, repo_path], check=True)
    branch_name = f"{clean_team}_{clean_leader}_AI_Fix"
    subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)

    return os.path.abspath(repo_path), branch_name