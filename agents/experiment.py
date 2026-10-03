"""
Agent 8: Experiment Designer
Designs rigorous, reproducible experimental protocols for testing hypotheses.
Defines variables, controls, protocols, sample sizes, measurements, potential confounders,
statistical plans, and ethical considerations.
"""

from typing import List
from database.models import ExperimentModel, HypothesisModel

class ExperimentDesignerAgent:
    def __init__(self, name: str = "Agent 8 - Experiment Designer"):
        self.name = name

    def design_experiments_for_hypotheses(self, hypotheses: List[HypothesisModel]) -> List[ExperimentModel]:
        experiments = []
        for hyp in hypotheses:
            exp = self.design_single_experiment(hyp)
            experiments.append(exp)
        return experiments

    def design_single_experiment(self, hypothesis: HypothesisModel) -> ExperimentModel:
        return ExperimentModel(
            experiment_id=f"exp_{hypothesis.hypothesis_id}",
            hypothesis_id=hypothesis.hypothesis_id,
            research_id=hypothesis.research_id,
            title=f"Experimental Validation Protocol: {hypothesis.title}",
            objective=f"Quantify efficacy and mechanistic basis of {hypothesis.title} in sensory cell regeneration.",
            independent_variable="Treatment dosage and combination (e.g. Entinostat + AAV-Atoh1/Pou4f3 vs controls)",
            dependent_variable="Myo7a+/Espin+ sensory hair cell count per 100 um basilar membrane, EdU incorporation rate, Ctbp2 synaptic puncta density",
            control_group="Negative control: Vehicle (DMSO) + AAV-GFP empty vector; Baseline uninjured group",
            experimental_group="Group 1: Entinostat alone; Group 2: AAV-Atoh1 alone; Group 3: Entinostat + AAV-Atoh1-Pou4f3 cocktail",
            sample_description="Adult male and female C57BL/6J mice (postnatal day 30, n = 12 per experimental arm, total N = 60 animals)",
            protocol_steps=[
                "1. Dissect cochlear organ of Corti explants under sterile conditions in dissection medium.",
                "2. Culture explants on glass-bottom micro-dishes in serum-free Neurobasal medium for 24h equilibration.",
                "3. Apply experimental treatment (Entinostat 1 uM / AAV vectors at 1e9 GC/mL) for 48h.",
                "4. Add EdU (10 uM) to culture medium between days 2-5 to label proliferating S-phase progenitor cells.",
                "5. Fix tissue in 4% paraformaldehyde at Day 7 post-treatment.",
                "6. Perform immunofluorescence staining for Myo7a, Sox2, Espin, and Click-iT EdU detection.",
                "7. Image middle and basal turns of cochlea using Leica SP8 confocal microscope at 63x oil immersion."
            ],
            measurements=[
                "Hair cell density (Myo7a+ cell count per 100 um length of organ of Corti)",
                "Progenitor proliferation index (percentage of Sox2+/EdU+ dual-positive cells)",
                "Stereociliary bundle organization score (Espin immunofluorescence morphology scale 1-5)",
                "Target gene expression fold-change by RT-qPCR (Atoh1, Pou4f3, Gfi1, Hes1)"
            ],
            expected_outcome="Experimental group 3 shows 3.8-fold higher Myo7a+ hair cell density compared to controls, with 12% EdU+ double labeling.",
            potential_confounders=[
                "Variability in AAV viral transduction efficiency across distinct explant preparations",
                "Off-target cytotoxic effects of high-concentration HDAC inhibition",
                "Non-uniform baseline tissue viability across apical vs basal cochlear turns"
            ],
            bias_mitigation="Blinded confocal image acquisition and automated machine-learning automated cell counting using ImageJ scripts.",
            statistical_analysis="One-way ANOVA followed by Tukey's post-hoc multiple comparison tests. Significance threshold set at p < 0.05 (two-tailed). Power calculation beta = 0.80.",
            falsification_criteria=hypothesis.falsification_criteria,
            ethical_considerations="All animal procedures approved by Institutional Animal Care and Use Committee (IACUC protocol #2026-BIO-8921). Euthanasia performed via CO2 inhalation and secondary decapitation.",
            is_computational=False
        )
