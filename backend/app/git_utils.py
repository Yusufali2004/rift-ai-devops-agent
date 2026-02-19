import os
import shutil
import subprocess

# RIFT REQUIREMENT: Isolated Sandbox
# We move the active work directory outside the project root to stop Uvicorn auto-reloads.
BASE_WORKSPACE = os.path.abspath("C:/rift-agent-workspace")

def setup_repo_isolated(repo_url, team_name, leader_name):
    """
    Clones the repository and prepares the mandatory RIFT branch.
    """
    # 1. Standardize Names (Upper case, underscores, specific suffix)
    clean_team = team_name.upper().replace(" ", "_")
    clean_leader = leader_name.upper().replace(" ", "_")
    branch_name = f"{clean_team}_{clean_leader}_AI_Fix"
    
    # 2. Define Sandbox Path
    os.makedirs(BASE_WORKSPACE, exist_ok=True)
    local_path = os.path.join(BASE_WORKSPACE, clean_team)
    
    # 3. Cleanup existing folder (Crucial for Windows file locking)
    if os.path.exists(local_path):
        # Using shell rmdir for a "force" delete on Windows
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", local_path], shell=True)

    # 4. Clone and Branch
    try:
        subprocess.run(["git", "clone", repo_url, local_path], check=True)
        # We use cwd to keep the FastAPI process stable in its own directory
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=local_path, check=True)
        print(f"✅ Sandbox Ready: {local_path} on branch {branch_name}")
        return local_path, branch_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Git Setup Error: {e}")
        raise e

def agent_commit(repo_path, message):
    """
    Mandatory RIFT Requirement: [AI-AGENT] prefix.
    """
    full_message = f"[AI-AGENT] {message}"
    
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", full_message], cwd=repo_path, check=True)
        print(f"📦 Committed: {full_message}")
    except subprocess.CalledProcessError:
        # Happens if the AI fix results in the exact same file content
        print("ℹ️ No changes detected to commit.")

def agent_push(repo_path, branch_name):
    """
    Pushes the fixed branch to the remote GitHub repository.
    """
    try:
        subprocess.run(["git", "push", "origin", branch_name], cwd=repo_path, check=True)
        print(f"🚀 Pushed {branch_name} to origin.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Push failed: {e}. Check your Git credentials.")