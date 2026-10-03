"""
Self-Correction Research Orchestrator for RESEARCH-OS.
Coordinates all 12 Agents through the complete scientific research workflow:
Understand Query -> Research Planner -> Literature Mining -> Evidence Critic -> Contradiction Detector -> Knowledge Graph -> Knowledge Gap Detector -> Hypothesis Engine -> Experiment Designer -> Computational Lab -> Red Team Scientist -> Iterative Self-Correction -> Research Synthesizer -> Reproducibility Engine.

Modes supported:
- QUICK_RESEARCH (fast literature & evidence synthesis)
- DEEP_RESEARCH (full multi-agent cycle with Red-Team criticism)
- RESEARCH_LAB (complete cycle + computational simulation + self-correction iteration)

Enforces strict anti-hallucination rules and medical safety disclaimers.
"""

import datetime
import uuid
import os
from typing import Dict, Any, List, Optional, Tuple

from database.models import (
    ScientificMemoryDB,
    ResearchSessionModel,
    PaperModel,
    HypothesisModel,
    HypothesisStatus,
    ExperimentModel,
    EvidenceLevel
)
from agents.planner import ResearchPlannerAgent, ResearchPlan
from agents.literature import LiteratureMinerAgent
from agents.evidence_critic import EvidenceCriticAgent, EvidenceProfile
from agents.contradiction import ContradictionDetectorAgent
from agents.knowledge_graph import KnowledgeGraphAgent, KnowledgeGraphData
from agents.gap_detector import KnowledgeGapDetectorAgent
from agents.hypothesis import HypothesisEngineAgent
from agents.experiment import ExperimentDesignerAgent
from agents.computational_lab import ComputationalLabAgent, SimulationResult
from agents.red_team import RedTeamScientistAgent, RedTeamCritique
from agents.synthesizer import ResearchSynthesizerAgent, FinalResearchReport
from agents.reproducibility import ReproducibilityEngineAgent

MEDICAL_SAFETY_DISCLAIMER = (
    "BIOMEDICAL RESEARCH NOTICE: RESEARCH-OS is an AI scientific research support tool designed for hypothesis generation and "
    "preclinical evidence analysis. Research Hypothesis ≠ Preclinical Evidence ≠ Clinical Evidence ≠ Medical Recommendation. "
    "This system does NOT prescribe medical treatment or provide clinical advice. All drug candidates and pathways must undergo "
    "formal Discovery -> In-Vitro -> Preclinical -> Toxicology -> Regulatory -> Clinical Trials validation."
)

class ResearchOrchestrator:
    def __init__(self, db_path: str = "database/research_memory.db"):
        self.db = ScientificMemoryDB(db_path)
        self.planner = ResearchPlannerAgent()
        self.miner = LiteratureMinerAgent()
        self.critic = EvidenceCriticAgent()
        self.contradiction_detector = ContradictionDetectorAgent()
        self.kg_engine = KnowledgeGraphAgent()
        self.gap_detector = KnowledgeGapDetectorAgent()
        self.hypothesis_engine = HypothesisEngineAgent()
        self.experiment_designer = ExperimentDesignerAgent()
        self.computational_lab = ComputationalLabAgent()
        self.red_team = RedTeamScientistAgent()
        self.synthesizer = ResearchSynthesizerAgent()
        self.reproducibility = ReproducibilityEngineAgent()

    def run_research_cycle(
        self,
        query: str,
        mode: str = "DEEP_RESEARCH",
        research_id: Optional[str] = None
    ) -> Dict[str, Any]:

        if not research_id:
            research_id = f"res_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(3).hex()}"

        logs: List[Dict[str, str]] = []

        def log_step(agent_name: str, action: str, details: str):
            ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
            logs.append({"timestamp": ts, "agent": agent_name, "action": action, "details": details})
            self.db.log_notebook(research_id, agent_name, action, details)

        log_step("Orchestrator", "START_RESEARCH_SESSION", f"Initiating {mode} for query: '{query}'")

        # Save session init
        session = ResearchSessionModel(
            research_id=research_id,
            query=query,
            mode=mode,
            status="IN_PROGRESS"
        )
        self.db.save_session(session)

        # 1. Research Planner
        log_step("Agent 1 - Planner", "FORMULATE_PLAN", "Decomposing research query into inclusion criteria and subquestions")
        plan: ResearchPlan = self.planner.plan(query)

        # 2. Literature Miner
        log_step("Agent 2 - Literature Miner", "MINE_LITERATURE", f"Searching Europe PMC & Crossref for keywords: {plan.keywords}")
        limit = 5 if mode == "QUICK_RESEARCH" else 10
        papers: List[PaperModel] = self.miner.mine_literature(plan.keywords, query, limit=limit)

        for paper in papers:
            self.db.save_paper(research_id, paper)
        log_step("Agent 2 - Literature Miner", "LITERATURE_STORED", f"Extracted {len(papers)} verified papers")

        # 3. Evidence Critic
        log_step("Agent 3 - Evidence Critic", "EVALUATE_EVIDENCE", "Evaluating sample size, study design, bias, and reproducibility")
        evidence_profiles: List[EvidenceProfile] = self.critic.evaluate_papers(papers)

        # 4. Contradiction Detector
        log_step("Agent 4 - Contradiction Detector", "DETECT_CONTRADICTIONS", "Analyzing divergent study findings and species/dosage differences")
        contradictions = self.contradiction_detector.detect_contradictions(papers)

        # 5. Knowledge Graph Engine
        log_step("Agent 5 - Knowledge Graph", "BUILD_KNOWLEDGE_GRAPH", "Constructing disease -> mechanism -> target -> gene -> drug graph network")
        kg_data: KnowledgeGraphData = self.kg_engine.build_graph(research_id, query)

        # 6. Knowledge Gap Detector
        log_step("Agent 6 - Gap Detector", "ISOLATE_KNOWLEDGE_GAPS", "Executing KNOWN -> UNKNOWN -> WHY UNKNOWN -> HOW TO TEST pipeline")
        gaps = self.gap_detector.detect_gaps(research_id, query)

        # 7. Hypothesis Engine
        log_step("Agent 7 - Hypothesis Engine", "GENERATE_HYPOTHESES", "Generating >=5 independent testable hypotheses with falsification criteria")
        hypotheses: List[HypothesisModel] = self.hypothesis_engine.generate_hypotheses(research_id, query)

        # 8. Experiment Designer
        log_step("Agent 8 - Experiment Designer", "DESIGN_EXPERIMENTS", "Formulating experimental protocols, controls, and statistical plans")
        experiments: List[ExperimentModel] = self.experiment_designer.design_experiments_for_hypotheses(hypotheses)

        # 9. Computational Lab (If mode is RESEARCH_LAB or DEEP_RESEARCH)
        simulations: List[SimulationResult] = []
        if mode in ["RESEARCH_LAB", "DEEP_RESEARCH"]:
            log_step("Agent 9 - Computational Lab", "EXECUTE_SIMULATION", "Executing Monte Carlo transcript dynamics & power analysis")
            for hyp in hypotheses[:2]:
                sim = self.computational_lab.run_simulation(hyp.hypothesis_id, hyp.title)
                simulations.append(sim)

        # 10. Red Team Scientist (Adversarial Critique)
        log_step("Agent 10 - Red Team Scientist", "ADVERSARIAL_CRITIQUE", "Subjecting hypotheses to independent adversarial critique")
        critiques: List[RedTeamCritique] = []
        for hyp in hypotheses:
            critique = self.red_team.critique_hypothesis(hyp)
            critiques.append(critique)

            # 15. SELF-CORRECTION LOOP: Update hypothesis status based on Red Team critique
            if critique.falsification_verdict == "WEAKENED":
                hyp.status = HypothesisStatus.WEAKENED
                hyp.status_reason = f"Red Team Critique: {critique.fatal_flaws[0]}"
                hyp.confidence_score = critique.revised_confidence_score
                log_step("Orchestrator - Self-Correction", "HYPOTHESIS_WEAKENED", f"Hypothesis '{hyp.hypothesis_id}' status updated to WEAKENED following critique")
            elif critique.falsification_verdict == "REFUTED":
                hyp.status = HypothesisStatus.REFUTED
                hyp.status_reason = f"Red Team Critique: {critique.fatal_flaws[0]}"
                hyp.confidence_score = critique.revised_confidence_score
                log_step("Orchestrator - Self-Correction", "HYPOTHESIS_REFUTED", f"Hypothesis '{hyp.hypothesis_id}' stored in Scientific Memory as FAILED HYPOTHESIS")
            else:
                hyp.status = HypothesisStatus.UNDER_REVIEW
                hyp.confidence_score = critique.revised_confidence_score

            # Save hypothesis (preserving active & failed hypotheses in memory)
            self.db.save_hypothesis(hyp)

        # 11. Research Synthesizer
        log_step("Agent 11 - Research Synthesizer", "SYNTHESIZE_REPORT", "Compiling scientific consensus, evidence summary, and research roadmap")
        report: FinalResearchReport = self.synthesizer.synthesize(
            research_id=research_id,
            query=query,
            papers=papers,
            evidence_profiles=evidence_profiles,
            contradictions=contradictions,
            gaps=gaps,
            hypotheses=hypotheses,
            experiments=experiments,
            critiques=critiques
        )

        # 12. Reproducibility Engine
        log_step("Agent 12 - Reproducibility Engine", "CREATE_MANIFEST", "Generating JSON Research Manifest & provenance checksums")
        source_dois = [p.doi for p in papers if p.doi]
        manifest = self.reproducibility.create_manifest(
            research_id=research_id,
            query=query,
            mode=mode,
            parameters={"query": query, "mode": mode, "keywords": plan.keywords},
            source_dois=source_dois,
            hypothesis_ids=[h.hypothesis_id for h in hypotheses],
            logs=logs
        )

        # Update session status to COMPLETED
        session.status = "COMPLETED"
        self.db.save_session(session)
        log_step("Orchestrator", "COMPLETE_RESEARCH_SESSION", f"Research session '{research_id}' successfully completed")

        return {
            "research_id": research_id,
            "query": query,
            "mode": mode,
            "disclaimer": MEDICAL_SAFETY_DISCLAIMER,
            "plan": plan.model_dump(),
            "papers": [p.model_dump() for p in papers],
            "evidence_profiles": [ep.model_dump() for ep in evidence_profiles],
            "contradictions": [c.model_dump() for c in contradictions],
            "knowledge_graph": kg_data.model_dump(),
            "knowledge_gaps": [g.model_dump() for g in gaps],
            "hypotheses": [h.model_dump() for h in hypotheses],
            "failed_hypotheses": self.db.get_failed_hypotheses(research_id),
            "experiments": [e.model_dump() for e in experiments],
            "simulations": [s.model_dump() for s in simulations],
            "red_team_critiques": [c.model_dump() for c in critiques],
            "lab_notebook": self.db.get_lab_notebook(research_id),
            "manifest": manifest.model_dump(),
            "final_report": report.model_dump()
        }
