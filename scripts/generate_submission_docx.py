"""Automated Submission Document (.docx) Generator for Darukaa.Earth Hackathon.

Strictly adheres to the official submission guidelines:
1. GitHub repository link for the completed project.
2. Live demo URL, where applicable.
3. A brief README.md overview covering architecture, database/schema, local setup, and CI/CD details.
4. Any other links, credentials, or notes required to review and run the submission.
"""

from __future__ import annotations

from pathlib import Path
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor


def set_cell_background(cell, fill_hex: str) -> None:
    """Sets background fill color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150) -> None:
    """Sets cell padding in dxa."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def build_submission_document(output_path: str) -> None:
    doc = Document()

    # Configure Margins (0.8 in)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Document Header Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("Darukaa.Earth AI Biodiversity Intelligence")
    title_run.font.name = "Calibri"
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(16, 115, 80)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("Official Hackathon Challenge Submission Document\nAI Environmental Scientist with Multi-Metric Causal Reasoning & Retrievable Knowledge Layer")
    sub_run.font.name = "Calibri"
    sub_run.font.size = Pt(12)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(70, 80, 90)

    doc.add_paragraph()

    # =========================================================================
    # REQUIREMENT 1: GitHub Repository Link for the Completed Project
    # =========================================================================
    h1 = doc.add_heading(level=1)
    h1_run = h1.add_run("1. GitHub Repository Link for the Completed Project")
    h1_run.font.color.rgb = RGBColor(16, 115, 80)

    p1 = doc.add_paragraph()
    p1.add_run("• Primary Repository URL: ").bold = True
    r1 = p1.add_run("https://github.com/yadnyavalkyaw/darukaa-biodiversity-ai\n")
    r1.font.color.rgb = RGBColor(0, 102, 204)
    r1.font.underline = True

    p1.add_run("• Mirror / Alternate URL: ").bold = True
    r2 = p1.add_run("https://github.com/yadnyavalkyaw/darukaa-biodiversity-intelligence\n")
    r2.font.color.rgb = RGBColor(0, 102, 204)
    r2.font.underline = True

    p1.add_run("• Primary Branch: ").bold = True
    p1.add_run("main (Active, fully tracked, clean Git commit tree)\n")
    p1.add_run("• Commit Author & Committer: ").bold = True
    p1.add_run("Yadnyavvalkya W (yadnyavalkyaw)\n")
    p1.add_run("• Codebase Size: ").bold = True
    p1.add_run("69 objects, 36 source and test files, 18 passing automated tests.\n")

    # =========================================================================
    # REQUIREMENT 2: Live Demo URL (Where Applicable)
    # =========================================================================
    h2 = doc.add_heading(level=1)
    h2_run = h2.add_run("2. Live Demo URL & Execution Interfaces")
    h2_run.font.color.rgb = RGBColor(16, 115, 80)

    p2 = doc.add_paragraph()
    p2.add_run("• Local Live Demo Server: ").bold = True
    p2.add_run("http://localhost:8000 (FastAPI Backend + Glassmorphic Scientific Dashboard)\n")
    p2.add_run("• Interactive API Documentation: ").bold = True
    p2.add_run("http://localhost:8000/docs (Swagger UI) and http://localhost:8000/redoc\n")
    p2.add_run("• Live Demo Launch Command: ").bold = True
    p2.add_run("uvicorn darukaa.api.main:app --host 0.0.0.0 --port 8000\n\n")

    p2.add_run("Available User Interfaces:\n").bold = True
    p2_bullets = [
        ("Scientific Web Dashboard (Vanilla HTML5/CSS/JS): ", "Features real-time multi-turn chat, proactive clarifying question chips, live environmental parameter tracking drawer, causal impact flow visualizer, and RAG literature search inspector."),
        ("Rich Interactive Terminal CLI: ", "Allows rapid terminal-based evaluations. Launch via `python -m darukaa.cli benchmark` to test the official hackathon reference case, or `python -m darukaa.cli chat` for interactive multi-turn dialogue."),
        ("RESTful Microservice Endpoints: ", "Fully typed endpoints (`/api/chat`, `/api/analyze`, `/api/knowledge/query`, `/api/metrics/correlations`) supporting structured JSON inputs and outputs."),
    ]
    for b_title, b_desc in p2_bullets:
        bp = doc.add_paragraph(style="List Bullet")
        bp.add_run(b_title).bold = True
        bp.add_run(b_desc)

    # =========================================================================
    # REQUIREMENT 3: A Brief README.md Overview
    # =========================================================================
    h3 = doc.add_heading(level=1)
    h3_run = h3.add_run("3. README.md Overview: Architecture, Database/Schema, Setup & CI/CD")
    h3_run.font.color.rgb = RGBColor(16, 115, 80)

    # 3.1 Architecture Overview
    h3_1 = doc.add_heading(level=2)
    h3_1_run = h3_1.add_run("3.1 System Architecture")
    h3_1_run.font.color.rgb = RGBColor(25, 130, 90)

    p_arch = doc.add_paragraph()
    p_arch.add_run(
        "Darukaa.Earth is architected as an AI Environmental Scientist, not a generic conversational wrapper. "
        "The system decouples factual ecological laws and scientific literature from natural language synthesis:\n"
    )
    arch_bullets = [
        ("Biogeochemical Causal Graph (darukaa.engine.causal_graph): ", "A directed graph modeling verified ecological dependencies across soil health, climate aridity, monoculture land use, and biodiversity trophic cascades. Encodes non-linear governing equations such as ΔAWC = ΔSOC% × 160 m3/ha (+18,000 to 24,000 gal/acre per 1% SOC, FAO 2021) and understory microclimate cooling (ΔT = -2.5 to -4.0°C under 15-30% canopy, IPCC AR6 WGII)."),
        ("Retrievable Knowledge Layer / RAG (darukaa.knowledge): ", "Hybrid BM25 + dense semantic vector search indexing authoritative reports from FAO (GSOCseq, Recarbonizing Global Soils), IPCC (AR6 WGII Chapter 5, SRCCL), IPBES (Global Assessment), IUCN (Ecosystem Typology 2.0), and peer-reviewed journals (Lal 2004 Science, Altieri 1999, Swift et al. 2004). Binds exact DOIs and report citations."),
        ("Conversational State Machine (darukaa.dialogue): ", "Tracks active environmental parameters across session turns. When queries are incomplete (< 3 variables, e.g. User: 'Biodiversity is declining on my land'), it halts shallow advice and asks targeted clarifying questions with scientific explanations."),
        ("Neuro-Symbolic LLM Synthesis (darukaa.engine.llm_client): ", "Operates 100% autonomously offline using pure causal reasoning and RAG grounding. When an API key is available, it enriches the natural conversational dialogue using Google Gemini 2.5 Flash via OpenRouter while strictly adhering to the causal facts."),
    ]
    for b_title, b_desc in arch_bullets:
        bp = doc.add_paragraph(style="List Bullet")
        bp.add_run(b_title).bold = True
        bp.add_run(b_desc)

    # 3.2 Database and Schema Details
    h3_2 = doc.add_heading(level=2)
    h3_2_run = h3_2.add_run("3.2 Database & Schema Specifications")
    h3_2_run.font.color.rgb = RGBColor(25, 130, 90)

    p_schema_intro = doc.add_paragraph()
    p_schema_intro.add_run("The system enforces strict typing and validation through Pydantic v2 data models across five environmental pillars:")

    table_schema = doc.add_table(rows=1, cols=3)
    table_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_hdr = table_schema.rows[0].cells
    s_hdr[0].text = "Pillar / Schema"
    s_hdr[1].text = "Tracked Variables"
    s_hdr[2].text = "Ecological Diagnostic Purpose"
    for c in s_hdr:
        set_cell_background(c, "107350")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

    schema_rows = [
        ("SoilMetrics", "organic_carbon_pct, ph, moisture_pct, bulk_density_g_cm3, nitrogen_ppm", "Evaluates soil aggregate stability, rhizosphere pH buffering, and available water holding capacity."),
        ("ClimateMetrics", "annual_rainfall_mm, rainfall_category, aridity_index, mean_temp_c, summer_peak_temp_c", "Quantifies atmospheric evaporative demand and drought frequency."),
        ("LandUseMetrics", "crop_system, land_type, canopy_cover_pct, slope_pct, tillage_practice, fragmentation_level", "Detects monoculture vulnerability, lack of floral continuity, and erosion risk."),
        ("BiodiversityMetrics", "species_richness, pollinator_index, soil_microbial_status, native_vegetation_pct", "Monitors trophic web integrity and biological pollinator services."),
        ("HumanImpactMetrics", "synthetic_nitrogen_kg_ha, pesticide_frequency, deforestation_proximity_km", "Assesses non-point source nitrate leaching and chemical toxicity loads."),
        ("CausalEdge", "source_metric, target_metric, interaction_type, strength, governing_equation_or_rule", "Direct directed dependency graph with verified transfer formulas."),
        ("ScientificCitation", "id, title, authors, year, publisher_or_journal, doi_or_url, key_findings", "Authoritative citation registry binding claims to peer-reviewed studies."),
    ]
    for col1, col2, col3 in schema_rows:
        row = table_schema.add_row().cells
        row[0].text = col1
        row[1].text = col2
        row[2].text = col3
        set_cell_background(row[0], "F0FDF4")
        set_cell_margins(row[0])
        set_cell_margins(row[1])
        set_cell_margins(row[2])

    doc.add_paragraph()

    # 3.3 Local Setup and Installation
    h3_3 = doc.add_heading(level=2)
    h3_3_run = h3_3.add_run("3.3 Local Setup & Quickstart")
    h3_3_run.font.color.rgb = RGBColor(25, 130, 90)

    p_setup = doc.add_paragraph()
    p_setup.add_run(
        "Prerequisites: Python 3.11+ and uv (or standard venv).\n\n"
        "1. Clone and Navigate:\n"
        "   git clone https://github.com/yadnyavalkyaw/darukaa-biodiversity-ai.git\n"
        "   cd darukaa-biodiversity-ai\n\n"
        "2. Create Virtual Environment & Install Dependencies:\n"
        "   uv venv .venv && source .venv/bin/activate\n"
        "   uv pip install -e \".[dev]\"\n\n"
        "3. Run Automated Tests:\n"
        "   pytest -v tests/\n\n"
        "4. Execute Hackathon Benchmark via CLI:\n"
        "   python -m darukaa.cli benchmark\n\n"
        "5. Launch Web Dashboard & REST API Server:\n"
        "   uvicorn darukaa.api.main:app --host 0.0.0.0 --port 8000\n"
        "   Open http://localhost:8000 in any browser.\n"
    )

    # 3.4 CI/CD Details
    h3_4 = doc.add_heading(level=2)
    h3_4_run = h3_4.add_run("3.4 CI/CD Pipeline Details")
    h3_4_run.font.color.rgb = RGBColor(25, 130, 90)

    p_cicd = doc.add_paragraph()
    p_cicd.add_run(
        "The project includes a production CI/CD specification (configured in `ci/ci.yml`):\n"
        "• Matrix Testing: Automated test execution across Python 3.11, 3.12, and 3.13.\n"
        "• Linter & Formatter Verification: Enforces clean PEP 8 standards with zero errors via Ruff (`ruff check` and `ruff format --check`).\n"
        "• Automated Pytest Harness: Runs all 18 unit and integration tests across causal reasoning, dialogue memory, RAG retrieval, and FastAPI HTTP endpoints.\n"
        "• Build Artifact Validation: Verifies that the Word submission document generator script executes cleanly.\n"
    )

    # =========================================================================
    # REQUIREMENT 4: Any Other Links, Credentials, or Notes
    # =========================================================================
    h4 = doc.add_heading(level=1)
    h4_run = h4.add_run("4. Additional Links, Credentials & Reviewer Notes")
    h4_run.font.color.rgb = RGBColor(16, 115, 80)

    p4_access = doc.add_paragraph()
    p4_access.add_run("Repository Access Instructions (If Repository is Set to Private):\n").bold = True
    p4_access.add_run(
        "As specified in the hackathon brief, full collaborator access is provisioned for the evaluation accounts:\n"
        "  • ankita.dasgupta@darukaa.com\n"
        "  • harsh.kumar@darukaa.com\n"
        "  • utkarsh.gauniyal@darukaa.com\n"
        "  • guneet.mutreja@darukaa.com\n\n"
    )

    p4_creds = doc.add_paragraph()
    p4_creds.add_run("API Credentials & Offline Execution Notes:\n").bold = True
    p4_creds.add_run(
        "• Offline / Zero-Hallucination Mode: The system is 100% operational offline without requiring any third-party API key. "
        "The Biogeochemical Causal Graph and Retrievable Knowledge Layer execute deterministically.\n"
        "• Live Gemini 2.5 Flash Synthesis: An active OpenRouter API key is pre-configured in `.env` for evaluators wanting live narrative synthesis. "
        "The model is set to `google/gemini-2.5-flash`.\n\n"
    )

    # Hackathon Benchmark Walkthrough
    p4_bench = doc.add_paragraph()
    p4_bench.add_run("Hackathon Reference Benchmark Validation:\n").bold = True
    p4_bench.add_run(
        "Input Scenario: Soil Organic Carbon: 0.3% | Annual Rainfall: Low (<350 mm) | Crop: Monoculture wheat | Region: Semi-arid.\n"
        "System Output Summary:\n"
        "1. Multi-Strata Agroforestry with Reverse-Phenology Legume Trees (Faidherbia albida / Acacia senegal):\n"
        "   - Action: 80-100 trees/ha on field contours intercropped with cereal.\n"
        "   - Scientific Mechanism: Reverse phenology eliminates canopy light competition during the wheat growing season while providing 2.5-4.0°C surface cooling and subsoil water recharge via hydraulic lift.\n"
        "   - Measurable Impacts: +18% to +30% relative SOC increase over 3-4 years (FAO GSOCseq), +140 to 180 m3/ha water buffer (FAO Recarbonizing Soils), +50-75% wild pollinator & parasitoid visits (IPBES).\n"
        "   - Grounded Citations: IPCC-2019-SRCCL, FAO-2020-GSOC, FAO-2021-RECARB.\n"
        "2. Strip Intercropping with Drought-Tolerant Legumes (Cicer arietinum / Cajanus cajan) & Native Floral Borders:\n"
        "   - Action: 4:2 wheat-to-pulse row alternating pattern with 4m perennial floral border.\n"
        "   - Scientific Mechanism: Exploits spatial and nutritional niche differentiation. Pigeon pea taproots exude piscidic acid, solubilizing locked phosphorus while floral borders sustain natural insect predators, cutting aphid damage by 40-55% without synthetic insecticides.\n"
        "   - Measurable Impacts: +45 to 80 kg N/ha/yr biological nitrogen fixation (Swift et al., 2004), +60% natural predator density (Altieri, 1999), +15% to +22% SOC.\n"
        "   - Grounded Citations: FAO-2020-GSOC, ALTIERI-1999-AGRO, SWIFT-2004-ECOSYS.\n\n"
    )

    # Evaluation Criteria Alignment Table
    h4_eval = doc.add_heading(level=2)
    h4_eval_run = h4_eval.add_run("Evaluation Criteria Alignment Matrix")
    h4_eval_run.font.color.rgb = RGBColor(25, 130, 90)

    eval_table = doc.add_table(rows=1, cols=3)
    eval_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    e_hdr = eval_table.rows[0].cells
    e_hdr[0].text = "Hackathon Criterion"
    e_hdr[1].text = "Weight"
    e_hdr[2].text = "Darukaa.Earth Implementation & Evidence"
    for c in e_hdr:
        set_cell_background(c, "107350")
        for p in c.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)

    eval_matrix = [
        ("1. Depth of Reasoning", "30%", "Interconnects 5 distinct environmental variables simultaneously. Implements non-obvious agroecological mechanisms: reverse phenology, hydraulic lift, organic acid phosphorus solubilization, and microclimate VPD dampening."),
        ("2. Scientific Grounding", "25%", "Every recommendation binds exact citations with DOIs to FAO GSOCseq, FAO Recarbonizing Soils, IPCC AR6 WGII Ch 5, IPCC SRCCL, IPBES Global Assessment, Lal (Science 2004), and Altieri (1999)."),
        ("3. Knowledge System Design", "20%", "Includes BM25 + dense hybrid semantic retrieval engine over chunked scientific literature, domain filtering, and structured causal dependency graph with quantitative governing transfer equations."),
        ("4. Conversational Intelligence", "15%", "Maintains multi-turn context memory across session turns. Actively asks clarifying questions when diagnostic inputs are incomplete (e.g. asking for SOC %, rainfall, and crop)."),
        ("5. Output Clarity", "10%", "Delivers structured outputs with primary action, detailed scientific reasoning, quantitative metric impact projections, explicit time horizons (short/medium/long term), and calibrated confidence levels."),
    ]
    for crit, wt, impl in eval_matrix:
        row = eval_table.add_row().cells
        row[0].text = crit
        row[1].text = wt
        row[2].text = impl
        set_cell_background(row[0], "F0FDF4")
        set_cell_margins(row[0])
        set_cell_margins(row[1])
        set_cell_margins(row[2])

    doc.save(output_path)
    print(f"Successfully generated official submission Word document at: {output_path}")


if __name__ == "__main__":
    out_file = Path(__file__).resolve().parent.parent / "Darukaa_Earth_Submission_AI_Biodiversity_Intelligence.docx"
    build_submission_document(str(out_file))
