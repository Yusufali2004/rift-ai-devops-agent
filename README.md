# RIFT 2026: Autonomous CI/CD Healing Agent
**Team Name:** Algo Ninjas  
**Leader:** Md Yusuf Ali

## 🚀 Live Demo & Video
- **Live Dashboard:** https://rift-ai-devops-agent.vercel.app
- **LinkedIn Demo:** [LinkedIn Post](https://www.linkedin.com/posts/md-yusuf-ali-_rift2026-activity-7430421159927537665-kiD0?utm_source=share&utm_medium=member_android&rcm=ACoAADodLfYBY_EZsUvRi6Nqo9dGHfrBOYTUpyA)
  

## 🏗 System Architecture
The system follows a **Self-Healing Loop** architecture designed for deterministic recovery.


1. **Trigger:** The React Dashboard initiates a `POST` request with the target repository.
2. **Environment Isolation:** The Backend clones the repository and initializes a dedicated branch: `TEAM_NAME_LEADER_NAME_AI_Fix`.
3. **Execution Sandbox:** Tests are discovered and executed via a sandboxed runner to prevent host-level side effects.
4. **Agentic Healing:**
   - **Analyzer:** Extracts stack traces and maps them to categories: `LINTING`, `SYNTAX`, `LOGIC`, `TYPE_ERROR`, `IMPORT`.
   - **Fixer (Gemini 1.5 Pro):** Ingests the error log and file context to generate a surgical code patch.
5. **Verification:** The system commits the fix with the `[AI-AGENT]` prefix and re-runs the test suite. This loop continues for a maximum of 5 iterations.

## 🛠 Tech Stack
- **Frontend:** React 18 (Functional Components + Hooks), Vite, Tailwind CSS, Lucide Icons.
- **Backend:** FastAPI (Async Orchestrator), GitPython (VCS Management), Pytest.
- **AI Engine:** Google Gemini 1.5 Pro (Leveraging 2M token context window).
- **Security:** OS-level path normalization and absolute path enforcement (WinError 3 protection).

## 📊 Scoring Methodology
Our agent optimizes for the RIFT 2026 scoring algorithm:
$$Score = 100 + (SpeedBonus) - (EfficiencyPenalty)$$
- **Base Score:** 100 points.
- **Speed Bonus:** +10 points if the agent resolves all failures in < 5 minutes.
- **Efficiency Penalty:** -2 points for every commit exceeding 20.

## 🧪 Complexity Analysis
- **Time Complexity:** $O(I \times (T + L))$  
  - $I$: Iterations (Max 5)  
  - $T$: Test execution time  
  - $L$: LLM Inference latency
- **Space Complexity:** $O(S)$ where $S$ is the size of the repository on disk.

## 🏷 Supported Failure Patterns
- **SYNTAX:** Auto-correction of missing colons, EOF errors, and bracket mismatches.
- **LOGIC:** Fixing assertion failures through algorithmic reasoning.
- **IMPORT/LINT:** Resolving missing dependencies and unused variable cleanup.

## ⚙️ Installation & Setup
### Prerequisites
- Python 3.10+
- Node.js 18+
- Gemini API Key (set in `backend/.env`)

### Steps
1. **Clone & Setup Backend:**
   ```bash
   cd backend
   # Create .env and add GEMINI_API_KEY=your_key
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload

2. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev


## 👥 Team Members

**Md Yusuf Ali**: Chief AI Architect & Backend Lead

**Md Arif Hossain**: Frontend Engineer & UI/UX
##

## Developed for the RIFT 2026 Hackathon — Autonomous Agentic Systems Track.
