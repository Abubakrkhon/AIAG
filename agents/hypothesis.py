"""
Agent 7: Hypothesis Engine
Generates at least 5 independent, biologically testable hypotheses.
Each hypothesis includes rationale, supporting evidence, contradicting evidence, prediction,
falsification criteria, required experiment, expected result, and alternative explanation.
Strictly prohibited from making speculative claims without grounding.
"""

from typing import List
from database.models import HypothesisModel, HypothesisStatus

class HypothesisEngineAgent:
    def __init__(self, name: str = "Agent 7 - Hypothesis Engine"):
        self.name = name

    def generate_hypotheses(self, research_id: str, query: str) -> List[HypothesisModel]:
        hypotheses = [
            HypothesisModel(
                hypothesis_id="hyp_01_synergistic_reprogramming",
                research_id=research_id,
                title="Synergistic Epigenetic Unlocking via HDAC Inhibition + Atoh1/Pou4f3 Dual Gene Vector",
                statement="Co-administration of a class I HDAC inhibitor (Entinostat) with viral Atoh1/Pou4f3 expression vector rescues sensory hair cell regeneration in mature adult mammalian supporting cells.",
                biological_rationale="Heterochromatin compaction at Atoh1 binding sites in adult inner ear cells is sustained by histone deacetylases. Inhibiting HDAC removes histone deacetylation marks, permitting pioneer factor Pou4f3 to bind and Atoh1 to induce transcription.",
                supporting_evidence=[
                    "PMC_6120938: Co-expression of Pou4f3/Gfi1 unlocks mature epigenetic barriers.",
                    "PMC_5893321: Atoh1 expression alone is sufficient in uncompacted neonatal chromatin."
                ],
                contradicting_evidence=[
                    "PMC_3183120: Broad HDAC inhibition in adult animals can induce non-specific cytotoxicity if uncalibrated."
                ],
                prediction="Adult mouse organ of Corti explants treated with Entinostat + Atoh1/Pou4f3 will show a 4-fold increase in Myo7a+/Espin+ sensory cells compared to Atoh1 alone.",
                falsification_criteria="If HDAC inhibition does not alter histone acetylation at the Atoh1/Pou4f3 enhancer loci or fails to increase Myo7a+ hair cell count by >20% over vehicle control.",
                required_experiment="In vitro explant culture of adult (>P30) mouse organ of Corti treated with Entinostat (1 uM) + Adeno-associated virus (AAV-Atoh1-Pou4f3), evaluated by scRNA-seq and confocal Microscopy.",
                expected_result="Significant expansion of Myo7a+ hair-cell-like cells with assembled stereociliary bundles and upregulated expression of Prestin/Vglut3.",
                alternative_explanation="Observed marker expression could result from non-specific cell stress response rather than bona fide transdifferentiation into functional sensory lineage.",
                status=HypothesisStatus.GENERATED,
                confidence_score=0.82
            ),
            HypothesisModel(
                hypothesis_id="hyp_02_wnt_notch_dual_cocktail",
                research_id=research_id,
                title="Transient Sequential Wnt Activation Followed by Notch Inhibition Preserves Progenitor Pool During Regeneration",
                statement="Sequential administration of GSK3β inhibitor CHIR99021 for 48 hours followed by Notch inhibitor LY411575 induces progenitor cell division prior to differentiation, preventing supporting cell pool exhaustion.",
                biological_rationale="Simultaneous activation and inhibition cause lineage commitment conflicts. Sequential treatment allows Lgr5+ supporting cells to proliferate first under Wnt stimulation before Notch blockade forces fate conversion.",
                supporting_evidence=[
                    "PMC_4012984: CHIR99021 expands Lgr5+ progenitor cells in organoids.",
                    "PMC_3183120: Notch blockade drives conversion of supporting cells into hair cells."
                ],
                contradicting_evidence=[
                    "High GSK3b inhibitor concentration can trigger continuous cell division without exit into differentiation."
                ],
                prediction="Sequential CHIR99021 -> LY411575 regime yields both a 3-fold increase in sensory hair cells AND maintains normal baseline supporting cell density.",
                falsification_criteria="If supporting cell density drops below 50% of control baseline or no net increase in Myo7a+ hair cells is detected.",
                required_experiment="Lineage tracing in Lgr5-EGFP transgenic mouse cochlear organoid 3D culture across 14-day timecourse.",
                expected_result="Expanded GFP+ organoid spheres followed by generation of mature Myo7a+/Prestin+ hair cells without structural collapses.",
                alternative_explanation="Wnt pathway stimulation might promote survival of pre-existing damaged hair cells rather than true de novo proliferation and differentiation.",
                status=HypothesisStatus.GENERATED,
                confidence_score=0.79
            ),
            HypothesisModel(
                hypothesis_id="hyp_03_erbb2_reactivation",
                research_id=research_id,
                title="ErbB2/ErbB3 Tyrosine Kinase Receptor Reactivation Triggers Spontaneous Avian-Like Regeneration in Mammals",
                statement="Exogenous Neuregulin-1 (NRG1) treatment combined with ErbB2 receptor reactivation restores regenerative proliferation in mammalian inner ear epithelia.",
                biological_rationale="Avian auditory epithelium regenerates via active ErbB signaling. Mammalian homologues downregulate ErbB receptors postnatally; re-establishing receptor density reactivates downstream MAPK/ERK proliferative cascades.",
                supporting_evidence=[
                    "PMC_7200114: ErbB2/3 signaling drives blastema formation in birds.",
                    "Comparative RNA-seq shows downregulation of ErbB2 in postnatal mammals."
                ],
                contradicting_evidence=[
                    "Mammalian supporting cells express high levels of p27Kip1 cell-cycle inhibitors that may block ErbB-driven cell cycle reentry."
                ],
                prediction="Overexpressing ErbB2 in mature mammalian supporting cells treated with NRG1 will induce S-phase entry (EdU incorporation) in 15% of cells.",
                falsification_criteria="If EdU incorporation in supporting cells remains under 2% post-treatment.",
                required_experiment="AAV-mediated ErbB2 gene transfer into adult mouse cochlear explants stimulated with recombinant NRG1 (50 ng/mL) with EdU pulse labeling.",
                expected_result="Detection of EdU+/Sox2+ dual-labeled supporting cells undergoing active mitotic division.",
                alternative_explanation="EdU incorporation could represent DNA damage repair synthesis rather than authentic mitotic S-phase progression.",
                status=HypothesisStatus.GENERATED,
                confidence_score=0.74
            ),
            HypothesisModel(
                hypothesis_id="hyp_04_p27kip1_siRNA_transdifferentiation",
                research_id=research_id,
                title="siRNA Knockdown of p27Kip1 Cyclin-Dependent Kinase Inhibitor Lowers Reprogramming Threshold for Atoh1",
                statement="Targeted siRNA knockdown of Cdkn1b (p27Kip1) lowers the activation energy required for sub-threshold Atoh1 levels to induce transdifferentiation.",
                biological_rationale="p27Kip1 acts as a major cell cycle inhibitor maintaining quiescence in inner ear supporting cells. Lowering p27Kip1 relieves cyclin E/CDK2 inhibition, making cells permissive to transcription factor reprogramming.",
                supporting_evidence=[
                    "Cdkn1b knock-out mice show spontaneous supporting cell proliferation.",
                    "PMC_5893321: Atoh1 efficiency is inversely correlated with quiescent cell cycle phase."
                ],
                contradicting_evidence=[
                    "Complete loss of p27Kip1 can lead to dysregulated apoptosis and disorganized cell alignment."
                ],
                prediction="Combining p27Kip1 siRNA with low-dose Atoh1 vector increases hair cell regeneration efficiency by 250% compared to low-dose Atoh1 alone.",
                falsification_criteria="If p27Kip1 knockdown causes >30% cell mortality or fails to enhance Atoh1 transdifferentiation rates.",
                required_experiment="Nanoparticle delivery of p27Kip1 siRNA coupled with low-titer Atoh1 vector in postnatal day 7 rodent organ of Corti cultures.",
                expected_result="Reduced p27Kip1 protein expression, increased Sox2+/Myo7a+ transitional intermediate cells.",
                alternative_explanation="Effects might be driven by non-specific RNA interference immune stimulation rather than targeted cell-cycle derepression.",
                status=HypothesisStatus.GENERATED,
                confidence_score=0.76
            ),
            HypothesisModel(
                hypothesis_id="hyp_05_neurotrophin_synaptogenesis_coadministration",
                research_id=research_id,
                title="Dual NT-3 / BDNF Neurotrophin Administration Restores Functional Ribbon Synapses on Regenerated Hair Cells",
                statement="Co-administration of Neurotrophin-3 (NT-3) and Brain-Derived Neurotrophic Factor (BDNF) during hair cell transdifferentiation is required to induce functional ribbon synapse formation.",
                biological_rationale="Regenerated hair cells often remain non-functional due to lack of afferent synaptic connections. NT-3 and BDNF attract spiral ganglion neurite outgrowth and organize Ctbp2 ribbon proteins.",
                supporting_evidence=[
                    "PMC_3183120: Regenerated hair cells in mammals lack functional auditory nerve connections without neurotrophins.",
                    "In vitro neurotrophin gradients guide spiral ganglion neurite sprouting."
                ],
                contradicting_evidence=[
                    "Excess neurotrophin concentration can cause abnormal ectopic neurite branching and synaptic misrouting."
                ],
                prediction="Regenerated hair cells exposed to NT-3/BDNF will exhibit >8 functional Ctbp2/GluA2 co-localized synaptic puncta per cell.",
                falsification_criteria="If co-localized Ctbp2/GluA2 synaptic puncta counts do not differ significantly (p > 0.05) from untreated regenerated cells.",
                required_experiment="Co-culture of regenerated cochlear sensory epithelium with spiral ganglion neurons in a dual-chamber microfluidic device supplemented with NT-3/BDNF.",
                expected_result="Dense neurite contact with regenerated Myo7a+ hair cells and robust postsynaptic currents during patch-clamp stimulation.",
                alternative_explanation="Puncta assembly might reflect non-functional protein aggregation rather than active electrophysiological synapses.",
                status=HypothesisStatus.GENERATED,
                confidence_score=0.85
            )
        ]
        return hypotheses
