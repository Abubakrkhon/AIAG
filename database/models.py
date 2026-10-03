"""
Database models and persistent scientific memory for RESEARCH-OS.
Tracks papers, claims, evidence levels, hypotheses (including FAILED_HYPOTHESIS history),
contradictions, experiments, knowledge graphs, and execution provenance logs.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import sqlite3
import json
import os
import datetime

class EvidenceLevel(str, Enum):
    FACT = "FACT"             # Confirmed factual baseline
    EVIDENCE = "EVIDENCE"     # Experimental/study finding from literature
    INFERENCE = "INFERENCE"   # AI logical synthesis from multiple sources
    HYPOTHESIS = "HYPOTHESIS" # Testable new hypothesis
    SPECULATION = "SPECULATION" # Speculative idea needing evidence

class HypothesisStatus(str, Enum):
    GENERATED = "GENERATED"
    UNDER_REVIEW = "UNDER_REVIEW"
    TESTING = "TESTING"
    SUPPORTED = "SUPPORTED"
    WEAKENED = "WEAKENED"
    REFUTED = "REFUTED"
    INCONCLUSIVE = "INCONCLUSIVE"

class PaperModel(BaseModel):
    paper_id: str
    title: str
    authors: List[str] = Field(default_factory=list)
    year: Optional[int] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    study_type: str = "Unknown"
    population: str = "N/A"
    intervention: str = "N/A"
    comparator: str = "N/A"
    outcome: str = "N/A"
    sample_size: str = "N/A"
    methodology: str = "N/A"
    limitations: str = "N/A"
    main_findings: str = "N/A"
    url: Optional[str] = None
    source: str = "Europe PMC"
    is_verified: bool = True

class ClaimModel(BaseModel):
    claim_id: str
    statement: str
    level: EvidenceLevel
    source_id: Optional[str] = None  # Paper ID or source tag
    confidence: float = 0.5
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class ContradictionModel(BaseModel):
    contradiction_id: str
    topic: str
    study_a_id: str
    study_a_finding: str
    study_b_id: str
    study_b_finding: str
    analysis: str
    potential_causes: List[str] = Field(default_factory=list)

class HypothesisModel(BaseModel):
    hypothesis_id: str
    research_id: str
    title: str
    statement: str
    biological_rationale: str
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    prediction: str
    falsification_criteria: str
    required_experiment: str
    expected_result: str
    alternative_explanation: str
    status: HypothesisStatus = HypothesisStatus.GENERATED
    status_reason: Optional[str] = None
    confidence_score: float = 0.5
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class ExperimentModel(BaseModel):
    experiment_id: str
    hypothesis_id: str
    title: str
    objective: str
    independent_variable: str
    dependent_variable: str
    control_group: str
    experimental_group: str
    sample_description: str
    protocol_steps: List[str] = Field(default_factory=list)
    measurements: List[str] = Field(default_factory=list)
    expected_outcome: str
    potential_confounders: List[str] = Field(default_factory=list)
    bias_mitigation: str
    statistical_analysis: str
    falsification_criteria: str
    ethical_considerations: str
    is_computational: bool = False

class KnowledgeNodeModel(BaseModel):
    node_id: str
    label: str
    type: str  # Disease, Mechanism, Target, Gene, Protein, Pathway, Drug, Experiment, Outcome
    source: str
    confidence: float
    evidence_level: EvidenceLevel
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

class KnowledgeEdgeModel(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation: str
    explanation: str
    confidence: float

class KnowledgeGapModel(BaseModel):
    gap_id: str
    known: str
    unknown: str
    why_unknown: str
    how_to_test: str

class ResearchSessionModel(BaseModel):
    research_id: str
    query: str
    mode: str = "DEEP_RESEARCH" # QUICK_RESEARCH, DEEP_RESEARCH, RESEARCH_LAB
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    model_version: str = "RESEARCH-OS-v1.0"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    status: str = "IN_PROGRESS"

class ScientificMemoryDB:
    def __init__(self, db_path: str = "database/research_memory.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()

            # Sessions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                research_id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                mode TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                model_version TEXT NOT NULL,
                parameters TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """)

            # Papers table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS papers (
                paper_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                title TEXT NOT NULL,
                authors TEXT NOT NULL,
                year INTEGER,
                doi TEXT,
                pmid TEXT,
                study_type TEXT,
                population TEXT,
                intervention TEXT,
                comparator TEXT,
                outcome TEXT,
                sample_size TEXT,
                methodology TEXT,
                limitations TEXT,
                main_findings TEXT,
                url TEXT,
                source TEXT,
                is_verified INTEGER NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Claims table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                claim_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                statement TEXT NOT NULL,
                level TEXT NOT NULL,
                source_id TEXT,
                confidence REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Contradictions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS contradictions (
                contradiction_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                study_a_id TEXT NOT NULL,
                study_a_finding TEXT NOT NULL,
                study_b_id TEXT NOT NULL,
                study_b_finding TEXT NOT NULL,
                analysis TEXT NOT NULL,
                potential_causes TEXT NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Hypotheses table (preserves active & failed hypotheses)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS hypotheses (
                hypothesis_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                title TEXT NOT NULL,
                statement TEXT NOT NULL,
                biological_rationale TEXT NOT NULL,
                supporting_evidence TEXT NOT NULL,
                contradicting_evidence TEXT NOT NULL,
                prediction TEXT NOT NULL,
                falsification_criteria TEXT NOT NULL,
                required_experiment TEXT NOT NULL,
                expected_result TEXT NOT NULL,
                alternative_explanation TEXT NOT NULL,
                status TEXT NOT NULL,
                status_reason TEXT,
                confidence_score REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Experiments table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                experiment_id TEXT PRIMARY KEY,
                hypothesis_id TEXT NOT NULL,
                research_id TEXT NOT NULL,
                title TEXT NOT NULL,
                objective TEXT NOT NULL,
                independent_variable TEXT NOT NULL,
                dependent_variable TEXT NOT NULL,
                control_group TEXT NOT NULL,
                experimental_group TEXT NOT NULL,
                sample_description TEXT NOT NULL,
                protocol_steps TEXT NOT NULL,
                measurements TEXT NOT NULL,
                expected_outcome TEXT NOT NULL,
                potential_confounders TEXT NOT NULL,
                bias_mitigation TEXT NOT NULL,
                statistical_analysis TEXT NOT NULL,
                falsification_criteria TEXT NOT NULL,
                ethical_considerations TEXT NOT NULL,
                is_computational INTEGER NOT NULL,
                FOREIGN KEY (hypothesis_id) REFERENCES hypotheses (hypothesis_id),
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Knowledge graph nodes
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS kg_nodes (
                node_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                label TEXT NOT NULL,
                type TEXT NOT NULL,
                source TEXT NOT NULL,
                confidence REAL NOT NULL,
                evidence_level TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Knowledge graph edges
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS kg_edges (
                edge_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                source_node_id TEXT NOT NULL,
                target_node_id TEXT NOT NULL,
                relation TEXT NOT NULL,
                explanation TEXT NOT NULL,
                confidence REAL NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Knowledge Gaps
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_gaps (
                gap_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                known TEXT NOT NULL,
                unknown TEXT NOT NULL,
                why_unknown TEXT NOT NULL,
                how_to_test TEXT NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            # Audit logs / Lab notebook
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS lab_notebook_entries (
                entry_id TEXT PRIMARY KEY,
                research_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (research_id) REFERENCES sessions (research_id)
            )
            """)

            conn.commit()

    def save_session(self, session: ResearchSessionModel):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO sessions (research_id, query, mode, timestamp, model_version, parameters, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session.research_id, session.query, session.mode, session.timestamp,
                session.model_version, json.dumps(session.parameters), session.status
            ))
            conn.commit()

    def save_paper(self, research_id: str, paper: PaperModel):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO papers (paper_id, research_id, title, authors, year, doi, pmid, study_type, population, intervention, comparator, outcome, sample_size, methodology, limitations, main_findings, url, source, is_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.paper_id, research_id, paper.title, json.dumps(paper.authors), paper.year,
                paper.doi, paper.pmid, paper.study_type, paper.population, paper.intervention,
                paper.comparator, paper.outcome, paper.sample_size, paper.methodology,
                paper.limitations, paper.main_findings, paper.url, paper.source, 1 if paper.is_verified else 0
            ))
            conn.commit()

    def save_hypothesis(self, hypothesis: HypothesisModel):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO hypotheses (hypothesis_id, research_id, title, statement, biological_rationale, supporting_evidence, contradicting_evidence, prediction, falsification_criteria, required_experiment, expected_result, alternative_explanation, status, status_reason, confidence_score, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hypothesis.hypothesis_id, hypothesis.research_id, hypothesis.title, hypothesis.statement,
                hypothesis.biological_rationale, json.dumps(hypothesis.supporting_evidence),
                json.dumps(hypothesis.contradicting_evidence), hypothesis.prediction,
                hypothesis.falsification_criteria, hypothesis.required_experiment,
                hypothesis.expected_result, hypothesis.alternative_explanation,
                hypothesis.status.value, hypothesis.status_reason, hypothesis.confidence_score,
                hypothesis.created_at, hypothesis.updated_at
            ))
            conn.commit()

    def log_notebook(self, research_id: str, agent_name: str, action: str, details: str):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            entry_id = f"nb_{datetime.datetime.now(datetime.timezone.utc).timestamp()}_{os.urandom(4).hex()}"
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            cursor.execute("""
            INSERT INTO lab_notebook_entries (entry_id, research_id, agent_name, action, details, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (entry_id, research_id, agent_name, action, details, ts))
            conn.commit()

    def get_session(self, research_id: str) -> Optional[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions WHERE research_id = ?", (research_id,))
            row = cursor.fetchone()
            if not row:
                return None
            res = dict(row)
            res['parameters'] = json.loads(res['parameters'])
            return res

    def get_hypotheses(self, research_id: str) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hypotheses WHERE research_id = ?", (research_id,))
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item['supporting_evidence'] = json.loads(item['supporting_evidence'])
                item['contradicting_evidence'] = json.loads(item['contradicting_evidence'])
                result.append(item)
            return result

    def get_failed_hypotheses(self, research_id: str) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hypotheses WHERE research_id = ? AND status IN ('REFUTED', 'WEAKENED')", (research_id,))
            rows = cursor.fetchall()
            result = []
            for r in rows:
                item = dict(r)
                item['supporting_evidence'] = json.loads(item['supporting_evidence'])
                item['contradicting_evidence'] = json.loads(item['contradicting_evidence'])
                result.append(item)
            return result

    def get_lab_notebook(self, research_id: str) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lab_notebook_entries WHERE research_id = ? ORDER BY timestamp ASC", (research_id,))
            return [dict(r) for r in cursor.fetchall()]
