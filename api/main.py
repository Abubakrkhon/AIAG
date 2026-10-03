"""
FastAPI Server for RESEARCH-OS.
Exposes REST endpoints for:
- Research workspace execution (/api/research/run)
- Session history & details (/api/research/session/{id})
- Literature search & verified paper details (/api/literature)
- Evidence map & bias profiles (/api/evidence)
- Knowledge Graph visualization endpoints (/api/knowledge_graph)
- Hypothesis database & status update management (/api/hypotheses)
- Red Team criticisms & lab notebook audit logs (/api/red_team, /api/notebook)
- Research manifest & Final scientific report download (/api/report)
"""

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from research.orchestrator import ResearchOrchestrator, MEDICAL_SAFETY_DISCLAIMER
from database.models import ScientificMemoryDB

app = FastAPI(
    title="RESEARCH-OS API",
    description="AI Scientific Research Agent Platform",
    version="1.0.0"
)

# Enable CORS for frontend interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = ResearchOrchestrator()
db = ScientificMemoryDB()

class ResearchRunRequest(BaseModel):
    query: str
    mode: str = "DEEP_RESEARCH" # QUICK_RESEARCH, DEEP_RESEARCH, RESEARCH_LAB

class HypothesisStatusUpdateRequest(BaseModel):
    hypothesis_id: str
    status: str
    status_reason: Optional[str] = None

@app.get("/api/health")
def health_check():
    return {"status": "ok", "system": "RESEARCH-OS", "version": "1.0.0"}

@app.post("/api/research/run")
def run_research(req: ResearchRunRequest):
    if not req.query or len(req.query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Research query must be provided.")

    valid_modes = ["QUICK_RESEARCH", "DEEP_RESEARCH", "RESEARCH_LAB"]
    mode = req.mode if req.mode in valid_modes else "DEEP_RESEARCH"

    try:
        results = orchestrator.run_research_cycle(req.query.strip(), mode=mode)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research execution failed: {str(e)}")

@app.get("/api/research/session/{research_id}")
def get_session_details(research_id: str):
    session = db.get_session(research_id)
    if not session:
        raise HTTPException(status_code=404, detail="Research session not found.")

    hypotheses = db.get_hypotheses(research_id)
    failed_hypotheses = db.get_failed_hypotheses(research_id)
    notebook = db.get_lab_notebook(research_id)

    return {
        "session": session,
        "hypotheses": hypotheses,
        "failed_hypotheses": failed_hypotheses,
        "notebook": notebook,
        "disclaimer": MEDICAL_SAFETY_DISCLAIMER
    }

@app.get("/api/hypotheses/{research_id}")
def get_hypotheses_db(research_id: str):
    hypotheses = db.get_hypotheses(research_id)
    return {
        "research_id": research_id,
        "hypotheses": hypotheses,
        "failed_hypotheses": [h for h in hypotheses if h["status"] in ["REFUTED", "WEAKENED"]]
    }

@app.post("/api/hypotheses/update_status")
def update_hypothesis_status(req: HypothesisStatusUpdateRequest):
    with db._get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hypotheses WHERE hypothesis_id = ?", (req.hypothesis_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Hypothesis ID not found.")

        cursor.execute("""
            UPDATE hypotheses
            SET status = ?, status_reason = ?
            WHERE hypothesis_id = ?
        """, (req.status, req.status_reason, req.hypothesis_id))
        conn.commit()

    return {"status": "success", "hypothesis_id": req.hypothesis_id, "new_status": req.status}

@app.get("/api/notebook/{research_id}")
def get_lab_notebook_logs(research_id: str):
    entries = db.get_lab_notebook(research_id)
    return {"research_id": research_id, "entries": entries}

# Serve frontend web interface
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
