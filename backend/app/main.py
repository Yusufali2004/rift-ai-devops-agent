import os
import time
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .schemas import RepoRequest, AgentResponse, FixDetail
from .git_utils import setup_repo, agent_commit
from .test_runner import discover_and_run_tests
from .agent_engine import get_llm_fix, apply_patch
from .scorer import calculate_final_score

app = FastAPI()

# Enable CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for the React dashboard to poll
results_db = {}

@app.post("/run-agent")
async def run_agent(request: RepoRequest, background_tasks: BackgroundTasks):
    job_id = f"{request.team_name}_{int(time.time())}"
    background_tasks.add_task(autonomous_loop, job_id, request)
    return {"job_id": job_id, "status": "started"}

@app.get("/results/{job_id}")
async def get_results(job_id: str):
    return results_db.get(job_id, {"status": "processing"})

async def autonomous_loop(job_id, request):
    start_time = time.time()
    all_fixes = []
    
    # 1. Setup & Branching
    repo_path, branch_name = setup_repo(request.repo_url, request.team_name, request.leader_name)
    
    status = "FAILED"
    for i in range(5):  # Mandatory 5-retry limit
        # 2. Run Tests
        logs, exit_code = discover_and_run_tests(repo_path)
        
        if exit_code == 0:
            status = "PASSED"
            break
        
        # 3. Fix Logic (Surgical LLM Call)
        # We assume the first .py or .js file mentioned in logs is the culprit
        # For a hackathon, we focus on 'main.py' or 'app.js' if not found
        target_file = "main.py" # Simple heuristic for the MVP
        
        with open(os.path.join(repo_path, target_file), "r") as f:
            content = f.read()
            
        fix_json = get_llm_fix(logs, content, "LOGIC/SYNTAX")
        apply_patch(repo_path, target_file, fix_json["fixed_code"])
        
        # 4. Commit with [AI-AGENT]
        agent_commit(repo_path, f"Retry {i+1}: {fix_json['explanation']}")
        
        all_fixes.append(FixDetail(
            file=target_file,
            bug_type="LOGIC",
            line=0,
            message=fix_json["explanation"],
            status="Fixed"
        ))

    end_time = time.time()
    final_score = calculate_final_score(start_time, end_time, len(all_fixes))

    # 5. Store Result
    results_db[job_id] = AgentResponse(
        repo_url=request.repo_url,
        team_name=request.team_name,
        team_leader=request.leader_name,
        branch_name=branch_name,
        total_failures=len(all_fixes),
        total_fixes=len(all_fixes),
        final_score=final_score,
        status=status,
        fixes=all_fixes,
        processing_time_seconds=round(end_time - start_time, 2)
    )