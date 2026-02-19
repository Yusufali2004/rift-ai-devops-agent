from pydantic import BaseModel
from typing import List, Optional

class FixDetail(BaseModel):
    file: str
    bug_type: str # LINTING, SYNTAX, etc.
    line: int
    message: str
    status: str # "Fixed" or "Failed"

class AgentResponse(BaseModel):
    repo_url: str
    team_name: str
    team_leader: str
    branch_name: str
    total_failures: int
    total_fixes: int
    final_score: int
    status: str # "PASSED" or "FAILED"
    fixes: List[FixDetail]
    processing_time_seconds: float