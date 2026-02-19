import os
import time
import uuid
import re
import json
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # Added for Step 3
from pydantic import BaseModel
from typing import Dict, List

from .git_utils import agent_commit, agent_push, setup_repo_isolated
from .test_runner import discover_and_run_tests
from .agent_engine import get_agent_fix, apply_patch
from .scorer import calculate_final_score

app = FastAPI(title="RIFT Autonomous DevOps Agent API")

# Define Results Path (Change 3)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Mount the results folder as a static route
app.mount("/results_static", StaticFiles(directory=RESULTS_FOLDER), name="results_static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: Dict[str, dict] = {}

class RepoRequest(BaseModel):
    repo_url: str
    team_name: str
    leader_name: str

@app.post("/run-agent")
async def start_agent(request: RepoRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "progress": "Initializing Agentic Loop...", "data": None}
    background_tasks.add_task(run_healing_loop, job_id, request)
    return {"job_id": job_id, "loading": True}

@app.get("/results/{job_id}")
async def get_results(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

def extract_failing_file(logs, repo_path):
    matches = re.findall(r'([\w/\.-]+\.py)', logs)
    for match in reversed(matches):
        clean = match.strip(".:")
        if "test_" in clean or "conftest" in clean:
            continue
        if os.path.exists(os.path.join(repo_path, clean)):
            return clean
    return "main.py"

async def run_healing_loop(job_id: str, request: RepoRequest):
    start_time = time.time()
    fixes: List[dict] = []
    timeline: List[dict] = []
    status = "FAILED"
    iteration_count = 0
    repo_path = ""

    try:
        repo_path, branch_name = setup_repo_isolated(request.repo_url, request.team_name, request.leader_name)

        for attempt in range(1, 6):
            iteration_count = attempt
            timestamp = time.strftime("%H:%M:%S")
            
            logs, exit_code = discover_and_run_tests(repo_path)
            
            timeline.append({
                "iteration": attempt,
                "timestamp": timestamp,
                "status": "PASSED" if exit_code == 0 else "FAILED"
            })

            if exit_code == 0:
                status = "PASSED"
                break

            target_file = extract_failing_file(logs, repo_path)
            with open(os.path.join(repo_path, target_file), "r", encoding="utf-8") as f:
                content = f.read()

            fix_data = get_agent_fix(logs, content)
            apply_patch(repo_path, target_file, fix_data["fixed_code"])

            commit_msg = f"Attempt {attempt}: Fixed {fix_data['bug_type']} in {target_file}"
            agent_commit(repo_path, commit_msg)

            fixes.append({
                "file": target_file,
                "bug_type": fix_data["bug_type"],
                "line_number": fix_data.get("line_number", 0),
                "commit_message": f"[AI-AGENT] {commit_msg}",
                "status": "✓ Fixed"
            })

        if len(fixes) > 0:
            agent_push(repo_path, branch_name)

        total_time = round(time.time() - start_time, 2)
        score_data = calculate_final_score(start_time, time.time(), len(fixes))

        # FINAL STRUCTURED OUTPUT FOR DASHBOARD
        results = {
            "run_summary": {
                "repository_url": request.repo_url,
                "team_name": request.team_name,
                "team_leader": request.leader_name,
                "branch_created": branch_name,
                "total_failures_detected": len(fixes) if status == "PASSED" else len(fixes) + 1,
                "total_fixes_applied": len(fixes),
                "final_status": status,
                "status_badge_color": "green" if status == "PASSED" else "red",
                "total_time_seconds": total_time
            },
            "score_breakdown": score_data, 
            "fixes_applied": fixes,
            "ci_cd_timeline": {
                "iterations_used": f"{iteration_count}/5",
                "timeline": timeline
            }
        }

        # Change 3: Save to project results folder
        with open(os.path.join(RESULTS_FOLDER, f"{job_id}.json"), "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["data"] = results

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["progress"] = str(e)