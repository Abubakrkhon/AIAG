document.addEventListener("DOMContentLoaded", () => {
    // Tab Navigation
    const navButtons = document.querySelectorAll(".nav-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            navButtons.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(pane => pane.classList.remove("active"));

            btn.classList.add("active");
            const targetTab = btn.getAttribute("data-tab");
            const activePane = document.getElementById(targetTab);
            if (activePane) {
                activePane.classList.add("active");
            }
        });
    });

    // Run Research Action
    const btnRunResearch = document.getElementById("btn-run-research");
    const btnQuickDemo = document.getElementById("btn-quick-demo");
    const queryInput = document.getElementById("research-query-input");
    const modeSelect = document.getElementById("research-mode-select");

    if (btnRunResearch) {
        btnRunResearch.addEventListener("click", () => {
            const query = queryInput.value.trim();
            const mode = modeSelect.value;
            if (!query) {
                alert("Please enter a valid research query.");
                return;
            }
            executeResearchSession(query, mode);
        });
    }

    if (btnQuickDemo) {
        btnQuickDemo.addEventListener("click", () => {
            queryInput.value = "Какие молекулярные механизмы связаны с регенерацией повреждённых сенсорных клеток?";
            modeSelect.value = "DEEP_RESEARCH";
            executeResearchSession(queryInput.value, "DEEP_RESEARCH");
        });
    }

    async function executeResearchSession(query, mode) {
        const sessionStatus = document.getElementById("session-status");
        const researchTag = document.getElementById("research-id-tag");
        const progressCard = document.getElementById("orchestration-progress-card");
        const resultsContainer = document.getElementById("workspace-summary-container");

        sessionStatus.textContent = "Multi-Agent Processing...";
        progressCard.classList.remove("hidden");
        resultsContainer.classList.add("hidden");

        // Simulate agent stepper progression
        animateStepper();

        try {
            const response = await fetch("/api/research/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query, mode: mode })
            });

            if (!response.ok) {
                throw new Error(`HTTP Error ${response.status}: ${await response.text()}`);
            }

            const data = await response.json();

            // Populate Research Session View
            renderResearchResults(data);

            sessionStatus.textContent = "Session Completed";
            researchTag.textContent = `ID: ${data.research_id}`;
            progressCard.classList.add("hidden");
            resultsContainer.classList.remove("hidden");

        } catch (err) {
            console.error("Research execution error:", err);
            alert(`Error executing research: ${err.message}`);
            sessionStatus.textContent = "Execution Error";
            progressCard.classList.add("hidden");
        }
    }

    function animateStepper() {
        const steps = [
            "step-agent-1", "step-agent-2", "step-agent-3", "step-agent-4",
            "step-agent-5", "step-agent-6", "step-agent-7", "step-agent-8",
            "step-agent-10", "step-agent-11"
        ];
        let idx = 0;
        const interval = setInterval(() => {
            if (idx > 0) {
                const prev = document.getElementById(steps[idx - 1]);
                if (prev) {
                    prev.classList.remove("active");
                    prev.classList.add("done");
                }
            }
            if (idx < steps.length) {
                const current = document.getElementById(steps[idx]);
                if (current) {
                    current.classList.add("active");
                }
                idx++;
            } else {
                clearInterval(interval);
            }
        }, 300);
    }

    function renderResearchResults(data) {
        // Workspace Summary Metrics
        document.getElementById("m-papers-count").textContent = data.papers ? data.papers.length : 0;
        document.getElementById("m-contradictions-count").textContent = data.contradictions ? data.contradictions.length : 0;
        document.getElementById("m-hypotheses-count").textContent = data.hypotheses ? data.hypotheses.length : 0;
        document.getElementById("m-confidence-score").textContent = data.final_report ? data.final_report.confidence_score : "0.82";

        document.getElementById("summary-text-content").textContent = data.final_report ? data.final_report.scientific_consensus : "Analysis complete.";

        // Literature Tab
        const litContainer = document.getElementById("literature-list");
        if (data.papers && data.papers.length > 0) {
            document.getElementById("lit-count-badge").textContent = `${data.papers.length} Papers`;
            litContainer.innerHTML = data.papers.map(p => `
                <div class="paper-item">
                    <div class="paper-title">${p.title}</div>
                    <div class="paper-authors">Authors: ${Array.isArray(p.authors) ? p.authors.join(", ") : p.authors} | Year: ${p.year || 'N/A'}</div>
                    <div class="paper-meta">
                        <span class="badge">${p.source}</span>
                        <span class="badge">DOI: ${p.doi || 'SOURCE NOT VERIFIED'}</span>
                        <span class="badge">Type: ${p.study_type}</span>
                    </div>
                    <div class="paper-abstract"><strong>Intervention:</strong> ${p.intervention}<br><strong>Outcome:</strong> ${p.outcome}<br><strong>Main Findings:</strong> ${p.main_findings}</div>
                </div>
            `).join("");
        }

        // Evidence Profiles Tab
        const evidenceContainer = document.getElementById("evidence-profiles-container");
        if (data.evidence_profiles && data.evidence_profiles.length > 0) {
            evidenceContainer.innerHTML = data.evidence_profiles.map(e => `
                <div class="paper-item">
                    <div class="paper-title">${e.title}</div>
                    <div class="paper-meta">
                        <span class="badge">Design: ${e.study_design}</span>
                        <span class="badge">Confidence: ${e.overall_confidence}</span>
                        <span class="badge">Reproducibility: ${e.reproducibility_rating}</span>
                    </div>
                    <div class="paper-abstract">
                        <strong>Sample Power:</strong> ${e.sample_size_score}<br>
                        <strong>Control Rigor:</strong> ${e.control_rigor}<br>
                        <strong>Key Limitations:</strong> ${e.key_limitations.join("; ")}
                    </div>
                </div>
            `).join("");
        }

        // Knowledge Graph Tab
        const kgNodes = document.getElementById("kg-nodes-list");
        const kgEdges = document.getElementById("kg-edges-list");
        if (data.knowledge_graph) {
            kgNodes.innerHTML = "<h3>Nodes</h3>" + data.knowledge_graph.nodes.map(n => `
                <div class="kg-node-card">
                    <strong>[${n.type}]</strong> ${n.label} <br>
                    <small>Source: ${n.source} | Level: ${n.evidence_level}</small>
                </div>
            `).join("");

            kgEdges.innerHTML = "<h3>Edges</h3>" + data.knowledge_graph.edges.map(e => `
                <div class="kg-node-card">
                    <strong>${e.source_node_id}</strong> → <em>${e.relation}</em> → <strong>${e.target_node_id}</strong><br>
                    <small>${e.explanation}</small>
                </div>
            `).join("");
        }

        // Hypotheses Tab
        const hypBody = document.getElementById("hypotheses-table-body");
        if (data.hypotheses && data.hypotheses.length > 0) {
            hypBody.innerHTML = data.hypotheses.map(h => `
                <tr>
                    <td><code>${h.hypothesis_id}</code></td>
                    <td><strong>${h.title}</strong><br><small>${h.statement}</small></td>
                    <td>${h.prediction}</td>
                    <td>${h.falsification_criteria}</td>
                    <td><span class="badge ${h.status === 'WEAKENED' || h.status === 'REFUTED' ? 'badge-warning' : ''}">${h.status}</span></td>
                    <td><strong>${h.confidence_score}</strong></td>
                </tr>
            `).join("");
        }

        // Experiments Tab
        const expContainer = document.getElementById("experiments-container");
        if (data.experiments && data.experiments.length > 0) {
            expContainer.innerHTML = data.experiments.map(exp => `
                <div class="paper-item">
                    <div class="paper-title">${exp.title}</div>
                    <div class="paper-abstract">
                        <strong>Objective:</strong> ${exp.objective}<br>
                        <strong>Independent Variable:</strong> ${exp.independent_variable}<br>
                        <strong>Dependent Variable:</strong> ${exp.dependent_variable}<br>
                        <strong>Sample:</strong> ${exp.sample_description}<br>
                        <strong>Statistical Analysis:</strong> ${exp.statistical_analysis}<br>
                        <strong>Ethical Considerations:</strong> ${exp.ethical_considerations}
                    </div>
                </div>
            `).join("");
        }

        // Red Team Tab
        const redteamContainer = document.getElementById("redteam-critiques-container");
        if (data.red_team_critiques && data.red_team_critiques.length > 0) {
            redteamContainer.innerHTML = data.red_team_critiques.map(c => `
                <div class="paper-item">
                    <div class="paper-title">${c.hypothesis_title}</div>
                    <div class="paper-meta">
                        <span class="badge badge-warning">Verdict: ${c.falsification_verdict}</span>
                        <span class="badge">Revised Score: ${c.revised_confidence_score}</span>
                    </div>
                    <div class="paper-abstract">
                        <strong style="color:var(--accent-rose);">Fatal Flaws / Toxicity Risks:</strong> ${c.fatal_flaws.join("; ")}<br>
                        <strong>Unsupported Assumptions:</strong> ${c.unsupported_assumptions.join("; ")}<br>
                        <strong>Alternative Explanations:</strong> ${c.alternative_explanations.join("; ")}
                    </div>
                </div>
            `).join("");
        }

        // Lab Notebook Tab
        const notebookContainer = document.getElementById("lab-notebook-logs");
        if (data.lab_notebook && data.lab_notebook.length > 0) {
            notebookContainer.innerHTML = data.lab_notebook.map(entry => `
                <div class="timeline-item">
                    <div class="timeline-time">${entry.timestamp}</div>
                    <div class="timeline-title">${entry.agent_name} - ${entry.action}</div>
                    <div class="timeline-details">${entry.details}</div>
                </div>
            `).join("");
        }

        // Final Report Tab
        const reportContainer = document.getElementById("report-rendered-view");
        if (data.final_report) {
            const r = data.final_report;
            reportContainer.innerHTML = `
                <h2>Scientific Research Report</h2>
                <p><strong>Research Query:</strong> ${r.query}</p>
                <p><strong>Research ID:</strong> ${r.research_id}</p>
                <hr style="margin:16px 0; border-color:var(--border-color);">

                <h3>1. Executive Summary</h3>
                <p>${r.executive_summary}</p>

                <h3>2. Scientific Consensus</h3>
                <p>${r.scientific_consensus}</p>

                <h3>3. Key Knowledge Gaps</h3>
                <ul>
                    ${r.knowledge_gaps.map(g => `<li><strong>Known:</strong> ${g.known} <br><strong>Unknown:</strong> ${g.unknown}</li>`).join("")}
                </ul>

                <h3>4. Ranked Hypotheses & Experimental Roadmap</h3>
                <ol>
                    ${r.candidate_hypotheses.map(h => `
                        <li>
                            <strong>${h.title}</strong> (Score: ${h.evidence_ranked_score}, Verdict: ${h.red_team_verdict})<br>
                            <em>${h.statement}</em>
                        </li>
                    `).join("")}
                </ol>

                <h3>5. Limitations & Safety Disclaimers</h3>
                <ul>
                    ${r.limitations_and_risks.map(l => `<li>${l}</li>`).join("")}
                </ul>
            `;
        }
    }
});
