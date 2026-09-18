# 🌍 Darukaa.Earth — AI Biodiversity Intelligence Chatbot

> **AI Environmental Scientist delivering multi-metric causal reasoning and evidence-grounded biodiversity restoration recommendations.**  
> *Developed for the Darukaa.Earth Hackathon Challenge.*

[![CI Pipeline](https://github.com/yadnyavalkyaw/darukaa-biodiversity-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/yadnyavalkyaw/darukaa-biodiversity-ai/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success.svg)](https://yadnyavalkyaw.github.io/darukaa-biodiversity-ai/)

> 🚀 **Live Interactive Demo**: **[https://yadnyavalkyaw.github.io/darukaa-biodiversity-ai/](https://yadnyavalkyaw.github.io/darukaa-biodiversity-ai/)**  
> *Zero setup required. Run instant ecological simulations, test multi-turn dialogue, search 12 indexed scientific literature sources, and inspect causal graphs directly in your browser.*

---

## 📑 Table of Contents
1. [Challenge Overview & Philosophy](#-challenge-overview--philosophy)
2. [System Architecture](#-system-architecture)
3. [Core Capabilities](#-core-capabilities)
   - [Multi-Metric Causal Model](#1-multi-metric-causal-model)
   - [Retrievable Scientific Knowledge Layer (RAG)](#2-retrievable-scientific-knowledge-layer-rag)
   - [Proactive Conversational Intelligence & Memory](#3-proactive-conversational-intelligence--memory)
   - [Evidence-Backed Quantitative Impact Forecasts](#4-evidence-backed-quantitative-impact-forecasts)
4. [Hackathon Benchmark Verification](#-hackathon-benchmark-verification)
5. [Database & Schema Specifications](#-database--schema-specifications)
6. [Local Quickstart & Execution](#-local-quickstart--execution)
7. [REST API Documentation](#-rest-api-documentation)
8. [Automated Testing & CI/CD](#-automated-testing--cicd)
9. [Submission & Reviewer Access](#-submission--reviewer-access)

---

## 🎯 Challenge Overview & Philosophy

Most generative AI chatbots fail at real-world environmental science because they generate shallow, generic advice (*"adopt sustainable practices"*) without considering multi-variable ecological constraints or providing verifiable evidence.

**Darukaa.Earth** is engineered from the ground up as an **AI Environmental Scientist**, not a generic chatbot. It couples:
- A **Biogeochemical Causal Graph** modeling non-linear interactions across soil chemistry, hydrology, microclimate, and trophic networks.
- A **Retrievable Knowledge Layer (RAG)** indexing authoritative peer-reviewed publications from the **FAO**, **IPCC**, **IPBES**, and **IUCN**.
- An active **State Machine** that prevents premature generic responses by proactively asking clarifying questions when diagnostic inputs are incomplete.
- **Zero-Hallucination Neuro-Symbolic Inference** that operates 100% autonomously offline without requiring external API keys, while supporting optional LLM narrative synthesis.

---

## 🏗️ System Architecture

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │               User Interaction Layer                   │
                                    │   - Scientific Web Dashboard (Glassmorphic Emerald UI) │
                                    │   - Rich Interactive Terminal CLI                      │
                                    │   - REST API (/api/chat, /api/analyze, etc.)          │
                                    └───────────────────────────┬────────────────────────────┘
                                                                │
                                                                ▼
                                    ┌────────────────────────────────────────────────────────┐
                                    │           Conversational State & Memory                │
                                    │   - Session Store & Turn Tracking                      │
                                    │   - Context Parameter Extractor (Regex + Semantic)     │
                                    │   - Clarifying Question Generator (Detects Gaps)       │
                                    └───────────────────────────┬────────────────────────────┘
                                                                │
                            ┌───────────────────────────────────┴───────────────────────────────────┐
                            ▼                                                                       ▼
┌───────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────────┐
│              Ecological Causal Graph                  │   │            Retrievable Knowledge Layer (RAG)          │
│   - Multi-Metric Causal Model (>= 3 variables)        │   │   - Curated Environmental Corpus                      │
│   - Stoichiometric & Ecological Transfer Functions    │   │     (FAO, IPCC AR6, IPBES, IUCN, Peer-Reviewed)       │
│   - Quantitative Metric Impact Forecasters            │   │   - Hybrid Dense & Lexical Vector Search              │
│   - Time Horizon & Confidence Calibrator              │   │   - Exact DOI / Report Citation Metadata              │
└───────────────────────────┬───────────────────────────┘   └───────────────────────────┬───────────────────────────┘
                            │                                                           │
                            └───────────────────────────┬───────────────────────────────┘
                                                        ▼
                                    ┌────────────────────────────────────────────────────────┐
                                    │         Scientific Grounding & Synthesis Engine        │
                                    │   - Non-Obvious Intervention Synthesizer               │
                                    │   - Evidence-Backed Justification Binder               │
                                    │   - Optional LLM Neuro-Symbolic Enhancer               │
                                    └───────────────────────────┬────────────────────────────┘
                                                                │
                                                                ▼
                                    ┌────────────────────────────────────────────────────────┐
                                    │                 Structured Response                    │
                                    │   - Actionable Agroecological Interventions            │
                                    │   - Multi-Metric Impact Table (SOC %, AWC, Pollinators)│
                                    │   - Time Horizons (Short, Medium, Long term)           │
                                    │   - Calibrated Confidence Score & Authoritative DOIs   │
                                    └────────────────────────────────────────────────────────┘
```

---

## 🔬 Core Capabilities

### 1. Multi-Metric Causal Model
The system explicitly links interconnected variables across 5 environmental pillars:
* **Soil Health**: Soil Organic Carbon (SOC %), pH, bulk density, moisture, microbial biomass carbon.
* **Climate Factors**: Annual precipitation (mm), aridity index ($P/PET$), temperature extremes, vapor pressure deficit (VPD).
* **Land Use**: Cropping pattern (monoculture vs. polyculture), woody canopy cover %, slope, tillage intensity.
* **Biodiversity Indicators**: Wild pollinator richness, predatory arthropod density, mycorrhizal fungi, soil macrofauna.
* **Human Chemical Impact**: Synthetic nitrogen application rate (kg N/ha), pesticide toxicity frequency, runoff risk.

#### Validated Transfer Functions:
* **Water Buffering**: $\Delta AWC = \Delta SOC\% \times 160\,\text{m}^3/\text{ha}$ ($+18,000$ to $24,000$ gallons/acre per 1% SOC) *(FAO 2021)*.
* **Thermal Dampening**: $\Delta T_{\text{surface}} = -2.0^\circ\text{C}$ to $-4.5^\circ\text{C}$ under $15\text{--}30\%$ agroforestry canopy *(IPCC AR6 WGII)*.
* **Biological Nitrogen**: Legume intercropping yields $50\text{--}120\,\text{kg N/ha/season}$ via active *Rhizobium* symbiosis *(Swift et al., 2004)*.
* **Pollinator Corridors**: Native floral margins occupying $5\text{--}8\%$ of field area boost wild pollinator richness by $50\text{--}80\%$ *(IPBES 2019)*.

### 2. Retrievable Scientific Knowledge Layer (RAG)
Unlike pure prompt-based systems, Darukaa indexes authoritative reports and journals:
- **FAO (2020)**: *Global Soil Organic Carbon Sequestration Potential Map (GSOCseq)* — [DOI: 10.4060/cb0353en](https://doi.org/10.4060/cb0353en)
- **FAO (2021)**: *Recarbonizing Global Soils: A Technical Manual of Recommended Management Practices* — [DOI: 10.4060/cb6378en](https://doi.org/10.4060/cb6378en)
- **IPCC (2022)**: *Climate Change 2022: Impacts, Adaptation and Vulnerability (AR6 WGII Chapter 5)* — [DOI: 10.1017/9781009325844.007](https://doi.org/10.1017/9781009325844.007)
- **IPCC (2019)**: *Special Report on Climate Change and Land (SRCCL)* — [Link](https://www.ipcc.ch/srccl/)
- **IPBES (2019)**: *Global Assessment Report on Biodiversity and Ecosystem Services* — [DOI: 10.5281/zenodo.3831673](https://doi.org/10.5281/zenodo.3831673)
- **IUCN (2020)**: *Global Ecosystem Typology 2.0* — [DOI: 10.2305/IUCN.CH.2020.13.en](https://doi.org/10.2305/IUCN.CH.2020.13.en)
- **Peer-Reviewed Journals**: Lal (Science, 2004); Swift et al. (2004); Altieri (1999); Paustian et al. (Nature, 2016); Tilman et al. (Nature, 2006).

### 3. Proactive Conversational Intelligence & Memory
When user queries lack sufficient environmental parameters, the system **halts shallow advice** and initiates a scientific clarification dialog:

```
User: "Biodiversity is declining on my land"

Darukaa Scientist: "To formulate evidence-backed, non-obvious recommendations tailored to your ecosystem,
I need a few critical diagnostic metrics:
Can you provide soil organic carbon %, rainfall pattern, and land use type?
(Why this matters: Soil organic carbon governs water retention and mycorrhizal networks,
rainfall dictates drought-resilient species selection, and land use identifies habitat fragmentation risks.)"
```

### 4. Evidence-Backed Quantitative Impact Forecasts
Every generated recommendation includes:
1. **Primary Action**: Exact species, spacing, seeding rates, and management steps.
2. **Scientific Reasoning**: Deep biogeochemical and trophic mechanisms.
3. **Multi-Metric Table**: Baselines vs. projected quantitative improvements.
4. **Time Horizons**: `short_term` (0–6 mo), `medium_term` (1–3 yrs), `long_term` (3–7+ yrs).
5. **Calibrated Confidence**: Calculated based on evidence support and parameter constraints.
6. **Authoritative Citations**: Direct report titles, authors, years, and DOIs.

---

## ⚡ Hackathon Benchmark Verification

**Benchmark Input:**
* Soil Organic Carbon: `0.3%`
* Annual Rainfall: `Low (<350 mm)`
* Cropping System: `Monoculture wheat`
* Ecoregion: `Semi-arid drylands`

**System Output Summary:**
1. **Multi-Strata Agroforestry with Reverse-Phenology Legume Trees (*Faidherbia albida* / *Acacia senegal*)**:
   - *Why it works*: *Faidherbia albida* drops its leaves during the wet cereal growing season (zero canopy competition), while leafing out during hot dry seasons to provide $2.5\text{--}4.0^\circ\text{C}$ surface cooling and subsoil water recharge via hydraulic lift.
   - *Impacted Metrics*:
     * **Soil Organic Carbon (SOC)**: $+18\%$ to $+30\%$ relative increase ($+0.25\%$ to $+0.45\%$ absolute) over 3–4 years (*FAO GSOCseq*).
     * **Available Water Capacity (AWC)**: $+140\text{--}180\,\text{m}^3/\text{ha}$ ($+18,000\text{--}24,000$ gal/acre) buffering capacity (*FAO Recarbonizing Soils*).
     * **Wild Pollinators & Avian Index**: $+50\text{--}75\%$ species richness increase (*IPBES*).
   - *Citations*: `IPCC-2019-SRCCL`, `FAO-2020-GSOC`, `FAO-2021-RECARB`.

2. **Strip Intercropping with Drought-Tolerant Legumes (*Cicer arietinum* / *Cajanus cajan*) & Native Floral Margins**:
   - *Why it works*: Niche differentiation where pigeon pea root exudates (*piscidic acid*) solubilize chemically locked phosphorus, while blooming strips attract parasitoid wasps and hoverflies to suppress aphid damage by $40\text{--}55\%$ without synthetic insecticides.
   - *Impacted Metrics*:
     * **Biological Nitrogen Influx**: $+45\text{--}80\,\text{kg N/ha/yr}$ biological fixation (*Swift et al., 2004*).
     * **Predatory Arthropod Density**: $+60\%$ higher natural predator populations (*Altieri, 1999*).
     * **Soil Organic Carbon**: $+15\text{--}22\%$ over 2–3 seasons (*FAO GSOCseq*).
   - *Citations*: `FAO-2020-GSOC`, `ALTIERI-1999-AGRO`, `SWIFT-2004-ECOSYS`.

---

## 📊 Database & Schema Specifications

Implemented with strict Pydantic v2 schemas (`darukaa.engine.metrics`):

| Schema | Key Fields | Purpose |
| :--- | :--- | :--- |
| `SoilMetrics` | `organic_carbon_pct`, `ph`, `moisture_pct`, `bulk_density_g_cm3`, `nitrogen_ppm` | Assesses rhizosphere health, aggregate stability, and nutrient availability. |
| `ClimateMetrics` | `annual_rainfall_mm`, `rainfall_category`, `aridity_index`, `mean_temperature_c` | Computes moisture deficits and thermal stress. |
| `LandUseMetrics` | `crop_system`, `land_type`, `canopy_cover_pct`, `slope_pct`, `tillage_practice` | Analyzes monoculture fragility, soil erosion, and vegetative shelter. |
| `BiodiversityMetrics` | `species_richness`, `pollinator_index`, `soil_microbial_status`, `native_vegetation_pct` | Monitors trophic web balance and biological pollinator services. |
| `HumanImpactMetrics`| `synthetic_nitrogen_kg_ha`, `pesticide_frequency_per_year` | Evaluates non-point source nitrate leaching and chemical toxicity. |
| `CausalEdge` | `source_metric`, `target_metric`, `interaction_type`, `strength`, `governing_equation_or_rule` | Encodes verified ecological laws and feedback loops. |
| `ScientificCitation`| `id`, `title`, `authors`, `year`, `publisher_or_journal`, `doi_or_url` | Manages exact peer-reviewed literature references. |

---

## 🚀 Local Quickstart & Execution

### Prerequisites
- Python 3.11, 3.12, or 3.13
- `uv` (recommended) or standard `python3 -m venv`

### Installation
```bash
# 1. Clone the repository
git clone https://github.com/yadnyavalkyaw/darukaa-biodiversity-ai.git
cd darukaa-biodiversity-ai

# 2. Create virtual environment using uv
uv venv .venv
source .venv/bin/activate

# 3. Install dependencies in editable mode
uv pip install -e ".[dev]"
```

### Running the Terminal CLI
```bash
# Run the Hackathon Benchmark Case (SOC 0.3%, low rain, monoculture wheat):
python -m darukaa.cli benchmark

# Run the interactive multi-turn terminal conversation:
python -m darukaa.cli chat

# Query the Retrievable Knowledge Layer directly:
python -m darukaa.cli query "soil organic carbon water capacity"
```

### Running the Web Dashboard & REST API
```bash
# Start the FastAPI server with live static dashboard:
uvicorn darukaa.api.main:app --host 0.0.0.0 --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in any modern browser to access the scientific web dashboard.

---

## 📡 REST API Documentation

FastAPI provides automatic interactive Swagger UI at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

### Core Endpoints

#### 1. Multi-Turn Conversational Reasoning
`POST /api/chat`
```json
{
  "message": "Soil organic carbon: 0.3%, rainfall: low, crop: monoculture wheat, region: semi-arid",
  "session_id": "session-123"
}
```
*Returns multi-variable analysis, proactive clarifying inquiries if inputs are incomplete, or full recommendations with citations.*

#### 2. Direct Structured Environmental Analysis
`POST /api/analyze`
```json
{
  "soil_organic_carbon_pct": 0.3,
  "annual_rainfall_mm": 320,
  "crop": "monoculture wheat",
  "region": "semi-arid"
}
```

#### 3. Retrievable Knowledge Layer Query
`POST /api/knowledge/query`
```json
{
  "query": "soil water holding capacity fao recarbonizing",
  "domain": "soil",
  "top_k": 3
}
```

#### 4. Ecological Causal Correlations
`GET /api/metrics/correlations`
*Returns the complete directed graph of ecological dependencies and governing transfer equations.*

#### 5. Health Probes
`GET /health`

---

## 🧪 Automated Testing & CI/CD

The system features an automated test suite covering causal reasoning, memory accumulation, RAG retrieval, and HTTP endpoints:

```bash
# Run pytest test suite:
pytest -v tests/

# Run ruff linting & format checks:
ruff check darukaa/ tests/
ruff format --check darukaa/ tests/
```

**Test Coverage:**
- `tests/test_causal_engine.py`: Verifies multi-metric reasoning ($\ge 3$ variables), transfer functions, and benchmark scenario.
- `tests/test_knowledge_retriever.py`: Verifies BM25 index scoring, domain filtering, and citation metadata binding.
- `tests/test_dialogue_state.py`: Verifies multi-turn memory accumulation and proactive clarifying inquiries.
- `tests/test_spatial_context.py`: Verifies coordinates and Köppen climate ecoregion mapping.
- `tests/test_api_endpoints.py`: Verifies FastAPI REST endpoints and standardized error envelopes.

---

## 📄 Submission & Reviewer Access

As specified in the hackathon guidelines, the submission includes the auto-generated Word document:
`Darukaa_Earth_Submission_AI_Biodiversity_Intelligence.docx`

To regenerate the official `.docx` submission document at any time:
```bash
python scripts/generate_submission_docx.py
```

### Collaborator Access (If Repository is Private)
Please ensure read/write collaborator invitations have been granted to:
* `ankita.dasgupta@darukaa.com`
* `harsh.kumar@darukaa.com`
* `utkarsh.gauniyal@darukaa.com`
* `guneet.mutreja@darukaa.com`

---

## ⚖️ License
MIT License. Developed for the Darukaa.Earth AI Biodiversity Intelligence Hackathon.
