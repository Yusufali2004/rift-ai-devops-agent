import os
import subprocess
import shutil

def setup_repo(repo_url, team_name, leader_name):
    # Branch format: TEAM_NAME_LEADER_NAME_AI_Fix
    clean_team = team_name.upper().replace(" ", "_")
    clean_leader = leader_name.upper().replace(" ", "_")
    branch_name = f"{clean_team}_{clean_leader}_AI_Fix"
    
    local_path = f"./temp_repos/{clean_team}"
    
    # Clear previous runs
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    
    # Clone and create branch
    subprocess.run(["git", "clone", repo_url, local_path], check=True)
    os.chdir(local_path)
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    
    return local_path, branch_name

def agent_commit(repo_path, message):
    os.chdir(repo_path)
    # Forced prefix
    full_message = f"[AI-AGENT] {message}"
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", full_message], check=True)
    # Note: We won't push until the final pass to avoid "commit noise"