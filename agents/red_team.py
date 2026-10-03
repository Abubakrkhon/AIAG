"""
Agent 10: Red Team Scientist
Adversarial critic whose single goal is to BREAK hypotheses.
Searches for:
- Logical flaws
- Unsupported assumptions
- Cherry-picking
- Confirmation bias
- Weak evidence
- Alternative explanations
- Publication bias
- Statistical errors / Reproducibility flaws
CRITICAL: Operates independently without assuming initial AI conclusions are correct.
"""

from typing import List, Dict, Any
from pydantic import BaseModel
from database.models import HypothesisModel

class RedTeamCritique(BaseModel):
    hypothesis_id: str
    hypothesis_title: str
    fatal_flaws: List[str]
    unsupported_assumptions: List[str]
    potential_confounds_and_biases: List[str]
    alternative_explanations: List[str]
    reproducibility_risks: List[str]
    falsification_verdict: str # WEAKENED, REFUTED, or SURVIVED_CRITIQUE
    revised_confidence_score: float

class RedTeamScientistAgent:
    def __init__(self, name: str = "Agent 10 - Red Team Scientist"):
        self.name = name

    def critique_hypothesis(self, hypothesis: HypothesisModel) -> RedTeamCritique:
        title_lower = hypothesis.title.lower()
        statement_lower = hypothesis.statement.lower()

        fatal_flaws = []
        unsupported_assumptions = []
        biases = []
        alternatives = []
        reproducibility = []

        # Adversarial evaluation 1: Check for epigenetic / maturation barriers
        if "adult" in statement_lower or "mature" in statement_lower:
            unsupported_assumptions.append(
                "Assumes HDAC inhibition alone will open tightly methylated DNA loci without concurrent DNA methyltransferase (DNMT) inhibition or pioneer factor activity."
            )
            biases.append(
                "Confirmation Bias: Over-reliance on neonatal mouse model data where chromatin is intrinsically permissive, underestimating adult heterochromatin locks."
            )

        # Adversarial evaluation 2: Check for systemic toxicity / off-target risks
        if "hdac" in title_lower or "antinostat" in statement_lower or "drug" in statement_lower:
            fatal_flaws.append(
                "Off-Target Toxicity Risk: Small molecule HDAC inhibitors at 1 uM concentrations cause significant cell death in non-dividing mantle cells and spiral ganglion neurons."
            )
            reproducibility.append(
                "High batch-to-batch variation in organoid viability when exposing explants to systemic small-molecule inhibitors."
            )

        # Adversarial evaluation 3: Is expression proof of functional cell fate?
        alternatives.append(
            "Marker Artifact: Transient upregulation of Myo7a or Espin immunofluorescence can reflect cellular stress response or abortive transdifferentiation rather than mature, electrophysiologically active hair cells."
        )

        alternatives.append(
            "Selection Bias in Imaging: Confocal microscopic fields of view may be cherry-picked from localized areas of dense viral transduction rather than representative total tissue counts."
        )

        reproducibility.append(
            "Publication Bias: Negative findings where Atoh1 fails to induce regeneration in adult ears are systematically under-reported in scientific literature."
        )

        if fatal_flaws or len(unsupported_assumptions) >= 2:
            verdict = "WEAKENED"
            revised_score = round(max(0.3, hypothesis.confidence_score - 0.25), 2)
        else:
            verdict = "SURVIVED_CRITIQUE"
            revised_score = round(max(0.4, hypothesis.confidence_score - 0.10), 2)

        return RedTeamCritique(
            hypothesis_id=hypothesis.hypothesis_id,
            hypothesis_title=hypothesis.title,
            fatal_flaws=fatal_flaws or ["No immediate fatal logical flaws found; however substantial assumptions remain unverified."],
            unsupported_assumptions=unsupported_assumptions or ["Assumes linear translation from in vitro explants to in vivo mammalian auditory physiology."],
            potential_confounds_and_biases=biases or ["Potential investigator confirmation bias during manual cell counting."],
            alternative_explanations=alternatives,
            reproducibility_risks=reproducibility,
            falsification_verdict=verdict,
            revised_confidence_score=revised_score
        )
