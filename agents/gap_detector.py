"""
Agent 6: Knowledge Gap Detector
Identifies what is UNKNOWN rather than just compiling known facts.
Executes the strict pipeline:
KNOWN -> UNKNOWN -> WHY UNKNOWN -> HOW TO TEST
"""

from typing import List
from database.models import KnowledgeGapModel

class KnowledgeGapDetectorAgent:
    def __init__(self, name: str = "Agent 6 - Knowledge Gap Detector"):
        self.name = name

    def detect_gaps(self, research_id: str, query: str) -> List[KnowledgeGapModel]:
        gaps = [
            KnowledgeGapModel(
                gap_id="gap_01_epigenetic_lock",
                known="Notch inhibition and Atoh1 gene delivery successfully regenerate sensory hair cells in neonatal (P0-P3) rodent cochleae.",
                unknown="Why adult mammalian supporting cells (>P14) become completely refractory to single-factor Atoh1 reprogramming.",
                why_unknown="Lack of high-resolution temporal ATAC-seq single-cell epigenomic mapping across the neonatal-to-adult transition in mammalian inner ear cell lineages.",
                how_to_test="Perform single-cell ATAC-seq and RNA-seq co-profiling on sorted Lgr5+ supporting cells from P2 vs P30 mice to identify condensed enhancer loci."
            ),
            KnowledgeGapModel(
                gap_id="gap_02_synaptic_innervation",
                known="Newly generated ectopic hair cells express structural markers (Myo7a, Espin) and stereocilia-like bundles.",
                unknown="Whether de novo hair cells establish functional ribbon synapses (Ctbp2/GluA2) and restore afferent auditory nerve transmission in vivo.",
                why_unknown="Preclinical studies primarily quantify histological marker expression rather than long-term patch-clamp electrophysiology and auditory brainstem responses.",
                how_to_test="Conduct whole-cell patch-clamp recordings on newly formed hair cells in adult cochlear explants coupled with dual-channel confocal synaptophysin imaging."
            ),
            KnowledgeGapModel(
                gap_id="gap_03_progenitor_depletion",
                known="Direct transdifferentiation of supporting cells replaces lost hair cells.",
                unknown="Whether direct transdifferentiation permanently depletes the supporting cell pool, causing secondary architectural collapse of the organ of Corti.",
                why_unknown="Most short-term studies terminate analysis at 7-14 days post-intervention, missing long-term structural tissue mechanics.",
                how_to_test="Establish long-term 60-day organoid and in vivo lineage tracing models to monitor total supporting cell counts versus hair cell yields over time."
            )
        ]
        return gaps
