"""
Automated testing suite for RESEARCH-OS.
Tests:
- Source verification & citation matching
- Hallucination detection ('SOURCE NOT VERIFIED' policy)
- Evidence extraction & bias scoring
- Contradiction detection
- Hypothesis generation & falsification criteria
- Experiment generation & computational lab disclaimers
- Database integrity & memory retention
"""

import pytest
import os
from database.models import ScientificMemoryDB, PaperModel, EvidenceLevel, HypothesisModel, HypothesisStatus
from agents.planner import ResearchPlannerAgent
from agents.literature import LiteratureMinerAgent
from agents.evidence_critic import EvidenceCriticAgent
from agents.contradiction import ContradictionDetectorAgent
from agents.knowledge_graph import KnowledgeGraphAgent
from agents.gap_detector import KnowledgeGapDetectorAgent
from agents.hypothesis import HypothesisEngineAgent
from agents.experiment import ExperimentDesignerAgent
from agents.computational_lab import ComputationalLabAgent
from agents.red_team import RedTeamScientistAgent
from agents.synthesizer import ResearchSynthesizerAgent
from agents.reproducibility import ReproducibilityEngineAgent
from research.orchestrator import ResearchOrchestrator

TEST_DB_PATH = "database/test_suite.db"

@pytest.fixture(autouse=True)
def cleanup_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    yield
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_source_verification_and_hallucination_prevention():
    miner = LiteratureMinerAgent()
    papers = miner.mine_literature(["atoh1", "notch"], "sensory hair cell regeneration", limit=5)

    assert len(papers) > 0
    for p in papers:
        assert p.paper_id is not None
        assert p.title is not None
        # Verify no unverified/fake source claims
        if not p.doi:
            assert p.source == "Europe PMC" or p.source == "Crossref" or "Verified" in p.source

def test_evidence_extraction_and_critic_evaluation():
    papers = [
        PaperModel(
            paper_id="PMC_123456",
            title="Atoh1 driving sensory hair cell regeneration in vitro",
            authors=["Smith A", "Doe B"],
            year=2023,
            doi="10.1038/s41586-023-00001-x",
            pmid="35000000",
            study_type="In Vitro Organoid Study",
            population="Neonatal mouse organ of Corti",
            intervention="Atoh1 overexpression",
            comparator="Empty vector control",
            outcome="3-fold increase in Myo7a+ hair cells",
            sample_size="n = 24 explants",
            methodology="Confocal microscopy and RT-qPCR",
            limitations="Neonatal tissue competence decays rapidly postnatally",
            main_findings="Atoh1 vector transfection drives support cell transdifferentiation.",
            url="https://doi.org/10.1038/s41586-023-00001-x",
            source="Nature",
            is_verified=True
        )
    ]
    critic = EvidenceCriticAgent()
    profiles = critic.evaluate_papers(papers)
    assert len(profiles) == 1
    p = profiles[0]
    assert p.evidence_level == EvidenceLevel.EVIDENCE
    assert p.overall_confidence > 0.5
    assert "bias_assessment" in p.model_dump()

def test_contradiction_detector():
    papers = [
        PaperModel(
            paper_id="P1", title="Avian sensory cell regeneration", authors=["Bird A"],
            population="Avian auditory tissue", outcome="Spontaneous regeneration", main_findings="Avian cells regenerate.", is_verified=True
        ),
        PaperModel(
            paper_id="P2", title="Mammalian inner ear failure", authors=["Mammal B"],
            population="Mammalian organ of Corti", outcome="Permanent cell loss", main_findings="Mammalian cells fail to regenerate.", is_verified=True
        )
    ]
    detector = ContradictionDetectorAgent()
    cntrs = detector.detect_contradictions(papers)
    assert len(cntrs) >= 1
    assert "Species" in cntrs[0].topic or "species" in cntrs[0].contradiction_id

def test_hypothesis_and_experiment_engine():
    hyp_engine = HypothesisEngineAgent()
    exp_engine = ExperimentDesignerAgent()

    hyps = hyp_engine.generate_hypotheses("res_001", "sensory cell regeneration")
    assert len(hyps) >= 5

    exps = exp_engine.design_experiments_for_hypotheses(hyps)
    assert len(exps) == len(hyps)

    for h in hyps:
        assert h.falsification_criteria is not None
        assert h.prediction is not None
        assert h.biological_rationale is not None

def test_computational_lab_disclaimer():
    comp_lab = ComputationalLabAgent()
    sim = comp_lab.run_simulation("hyp_01", "HDAC inhibition + Atoh1 vector")
    assert "COMPUTATIONAL SIMULATION - NOT CLINICAL PROOF" in sim.disclaimer

def test_red_team_adversarial_critique():
    hyp = HypothesisModel(
        hypothesis_id="hyp_test", research_id="res_test", title="HDAC inhibition in adult mouse",
        statement="HDAC inhibitor Entinostat cures hearing loss in adult mice.",
        biological_rationale="Opens chromatin.", supporting_evidence=["PMC_1234"],
        contradicting_evidence=[], prediction="100% recovery",
        falsification_criteria="No recovery", required_experiment="In vivo injection",
        expected_result="Full recovery", alternative_explanation="Toxicity",
        confidence_score=0.85
    )
    red_team = RedTeamScientistAgent()
    critique = red_team.critique_hypothesis(hyp)
    assert critique.falsification_verdict in ["WEAKENED", "REFUTED", "SURVIVED_CRITIQUE"]
    assert len(critique.fatal_flaws) > 0 or len(critique.unsupported_assumptions) > 0

def test_database_integrity_and_memory():
    db = ScientificMemoryDB(TEST_DB_PATH)
    hyp = HypothesisModel(
        hypothesis_id="h1", research_id="r1", title="Test Hyp", statement="Test statement",
        biological_rationale="Rationale", supporting_evidence=["e1"], contradicting_evidence=["e2"],
        prediction="Pred", falsification_criteria="Falsify", required_experiment="Exp",
        expected_result="Result", alternative_explanation="Alt", status=HypothesisStatus.WEAKENED,
        confidence_score=0.5
    )
    db.save_hypothesis(hyp)

    active_hyps = db.get_hypotheses("r1")
    failed_hyps = db.get_failed_hypotheses("r1")

    assert len(active_hyps) == 1
    assert len(failed_hyps) == 1
    assert failed_hyps[0]["status"] == "WEAKENED"

def test_full_orchestration_cycle():
    orch = ResearchOrchestrator(TEST_DB_PATH)
    res = orch.run_research_cycle("Какие молекулярные механизмы связаны с регенерацией повреждённых сенсорных клеток?", mode="QUICK_RESEARCH")

    assert res["research_id"] is not None
    assert len(res["papers"]) > 0
    assert len(res["hypotheses"]) >= 5
    assert len(res["experiments"]) >= 5
    assert res["final_report"]["scientific_consensus"] is not None
    assert res["manifest"]["research_id"] == res["research_id"]
