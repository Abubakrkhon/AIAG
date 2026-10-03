"""
Agent 1: Research Planner
Formulates research objectives, inclusion/exclusion criteria, keywords, synonyms,
search strategies, subquestions, required datasets, and candidate methodologies.
"""

from typing import List, Dict, Any
from pydantic import BaseModel

class ResearchPlan(BaseModel):
    query: str
    objective: str
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    keywords: List[str]
    synonyms: Dict[str, List[str]]
    search_strategy: str
    subquestions: List[str]
    required_datasets: List[str]
    candidate_methodologies: List[str]

class ResearchPlannerAgent:
    def __init__(self, name: str = "Agent 1 - Research Planner"):
        self.name = name

    def plan(self, research_question: str) -> ResearchPlan:
        """
        Analyzes the research question and structures a formal research plan.
        """
        # Parse key entities from query for targeted search expansion
        keywords = self._extract_keywords(research_question)
        synonyms = self._generate_synonyms(keywords)
        subquestions = self._generate_subquestions(research_question)

        objective = f"Systematically investigate and evaluate scientific evidence regarding: {research_question}"

        inclusion_criteria = [
            "Peer-reviewed studies, systematic reviews, clinical trials, or validated preprints (bioRxiv/arXiv)",
            "Studies evaluating biological, molecular, cellular, or pharmacological mechanisms",
            "Articles with clear methodologies, quantitative sample sizes, and reported effect sizes/p-values"
        ]

        exclusion_criteria = [
            "Unverified opinions, non-peer-reviewed blog posts, or media articles lacking citations",
            "Studies with undisclosed methodologies or insufficient data reporting",
            "Duplicate studies or purely speculative commentary without mechanistic evidence"
        ]

        search_strategy = (
            f"Multi-database search across PubMed, Europe PMC, Crossref, and arXiv using boolean expanded terms: "
            f"({' OR '.join(keywords)}) AND (mechanism OR pathway OR regeneration OR efficacy)"
        )

        required_datasets = [
            "Single-cell RNA sequencing (scRNA-seq) gene expression profiles",
            "Proteomic expression datasets",
            "Clinical or animal model trial outcomes"
        ]

        candidate_methodologies = [
            "Differential gene expression analysis",
            "Pathway enrichment analysis (KEGG/GO)",
            "Molecular docking & structural target modeling",
            "Meta-analytic synthesis & evidence bias scoring"
        ]

        return ResearchPlan(
            query=research_question,
            objective=objective,
            inclusion_criteria=inclusion_criteria,
            exclusion_criteria=exclusion_criteria,
            keywords=keywords,
            synonyms=synonyms,
            search_strategy=search_strategy,
            subquestions=subquestions,
            required_datasets=required_datasets,
            candidate_methodologies=candidate_methodologies
        )

    def _extract_keywords(self, query: str) -> List[str]:
        words = query.replace('?', '').replace('.', '').replace(',', '').split()
        stopwords = {'why', 'how', 'what', 'which', 'are', 'is', 'the', 'in', 'and', 'or', 'for', 'with', 'related', 'associated', 'Какие', 'молекулярные', 'механизмы', 'связаны', 'с'}
        kw = [w.strip() for w in words if w.lower() not in stopwords and len(w) > 2]
        if not kw:
            kw = ["sensory", "cell", "regeneration", "pathway"]
        return kw

    def _generate_synonyms(self, keywords: List[str]) -> Dict[str, List[str]]:
        syn_map = {
            "sensory": ["hair cells", "inner ear", "photoreceptor", "tactile receptor"],
            "regeneration": ["repair", "re-differentiation", "proliferation", "stem cell activation"],
            "cells": ["cellular", "tissue", "phenotype"],
            "клеток": ["hair cells", "sensory receptors", "epithelium"],
            "регенерацией": ["regeneration", "repair", "restoration"]
        }
        res = {}
        for k in keywords:
            res[k] = syn_map.get(k.lower(), [f"{k} signaling", f"{k} pathway"])
        return res

    def _generate_subquestions(self, query: str) -> List[str]:
        return [
            f"What specific signaling pathways are activated or suppressed during this process?",
            f"Which transcription factors or key proteins trigger cellular reprogramming/regeneration?",
            f"Are there contrasting findings across species (e.g., mammals vs. birds/zebrafish)?",
            f"What experimental interventions or pharmacological targets have been shown to induce regeneration?"
        ]
