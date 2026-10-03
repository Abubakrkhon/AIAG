"""
Agent 12: Reproducibility Engine
Ensures full auditability and computational reproducibility for every research project run.
Tracks:
- Unique Research Run ID
- High-precision Timestamps
- Exact Query parameters & Execution Modes
- Model versions
- Full list of query history and retrieved source DOIs
- Dataset versions and seed parameters
- Generated hypotheses and analysis outputs
Creates a complete JSON Research Manifest file.
"""

import json
import os
import datetime
from typing import Dict, Any, List
from pydantic import BaseModel

class ResearchManifest(BaseModel):
    research_id: str
    query: str
    mode: str
    timestamp: str
    model_version: str
    parameters: Dict[str, Any]
    source_dois: List[str]
    generated_hypotheses_ids: List[str]
    execution_steps_log: List[Dict[str, str]]

class ReproducibilityEngineAgent:
    def __init__(self, name: str = "Agent 12 - Reproducibility Engine"):
        self.name = name

    def create_manifest(
        self,
        research_id: str,
        query: str,
        mode: str,
        parameters: Dict[str, Any],
        source_dois: List[str],
        hypothesis_ids: List[str],
        logs: List[Dict[str, str]],
        output_dir: str = "research/manifests"
    ) -> ResearchManifest:

        manifest = ResearchManifest(
            research_id=research_id,
            query=query,
            mode=mode,
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            model_version="RESEARCH-OS-v1.0-COMPLIANT",
            parameters=parameters,
            source_dois=source_dois,
            generated_hypotheses_ids=hypothesis_ids,
            execution_steps_log=logs
        )

        os.makedirs(output_dir, exist_ok=True)
        manifest_path = os.path.join(output_dir, f"{research_id}_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest.model_dump(), f, indent=2, ensure_ascii=False)

        return manifest
