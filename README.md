# RIFT 2026: Autonomous CI/CD Healing Agent
**Team Name:** [Your Team Name]
**Leader:** [Your Name]

## 🚀 Live Demo & Video
- **Live Dashboard:** [Insert Vercel Link]
- **LinkedIn Demo:** [Insert LinkedIn Video Link]

## 🛠 Tech Stack
- **Frontend:** React (Hooks + Functional Components), Tailwind CSS, Shadcn/UI.
- **Backend:** FastAPI (Python), Docker (Sandboxed Execution).
- **AI Engine:** Gemini 1.5 Pro (Multi-agent Orchestration via LangGraph logic).

## 🏗 System Architecture
1. **Trigger:** Dashboard sends GitHub URL to FastAPI.
2. **Analysis:** Backend clones repo into a Docker sandbox and runs `pytest/npm test`.
3. **Healing:** Analyzer identifies bug types (LINTING, SYNTAX, etc.). Fixer Agent generates surgical patches.
4. **Verification:** Agent commits with `[AI-AGENT]` prefix and retries until tests pass (Max 5).

## 📊 Suspicion & Scoring
- **Base Score:** 100
- **Speed Bonus:** +10 (under 5 mins)
- **Efficiency:** -2 per commit over 20.

## ⚙️ Installation
1. `cd backend && pip install -r requirements.txt`
2. `python -m uvicorn app.main:app --reload`
3. `cd frontend && npm install && npm run dev`