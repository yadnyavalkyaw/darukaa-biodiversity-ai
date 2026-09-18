"""OpenRouter LLM Integration for Darukaa.Earth AI Biodiversity Intelligence.

Enriches scientific dialogue and narrative synthesis using Google Gemini 2.5 Flash
via OpenRouter, while preserving strict scientific grounding, multi-metric constraints,
and exact FAO/IPCC citations.
"""

from __future__ import annotations

import logging
import os

import httpx
from dotenv import load_dotenv

from darukaa.engine.reasoner import ScientificAnalysisResult

load_dotenv(override=True)
logger = logging.getLogger(__name__)


class OpenRouterLLMClient:
    """Client for OpenRouter API with graceful fallback to deterministic scientific reasoning."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("LLM_MODEL", "google/gemini-2.5-flash")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_key.startswith("sk-or-"))

    def synthesize_conversational_response(
        self,
        user_message: str,
        analysis_result: ScientificAnalysisResult,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> str:
        """Uses Gemini 2.5 Flash to synthesize an environmental scientist response

        based strictly on the deterministic causal graph results and retrieved literature.
        """
        if not self.is_available():
            return self._build_deterministic_summary(analysis_result)

        # Build grounded system prompt
        system_prompt = (
            "You are the Darukaa.Earth Senior AI Environmental Scientist. "
            "You provide rigorous, non-obvious, evidence-backed agroecological reasoning. "
            "STRICT GROUNDING RULES:\n"
            "1. Base all quantitative claims, mechanisms, and interventions strictly on the provided Causal Graph and Literature.\n"
            "2. Never recommend vague practices like 'adopt sustainable agriculture'. Always cite exact species (e.g. Faidherbia albida, Cicer arietinum), mechanisms (reverse phenology, hydraulic lift, biological N fixation), and quantitative metrics.\n"
            "3. Explicitly connect at least 3 environmental variables (Soil Carbon, Rainfall, Cropping, Biodiversity).\n"
            "4. Cite the provided authoritative sources (FAO GSOCseq, IPCC AR6 WGII, IPBES) with exact findings.\n"
            "5. Keep tone authoritative, scientific, clear, and actionable."
        )

        context_data = {
            "parcel_summary": analysis_result.parcel_summary,
            "connected_variables": analysis_result.variable_connections,
            "vulnerabilities": analysis_result.critical_vulnerabilities,
            "recommendations": [
                {
                    "title": r.title,
                    "action": r.primary_action,
                    "reasoning": r.scientific_reasoning,
                    "pathway": r.ecological_pathway,
                    "impacts": [
                        {
                            "metric": i.metric_name,
                            "improvement": i.projected_improvement,
                            "horizon": i.time_horizon.value,
                            "mechanism": i.mechanism,
                        }
                        for i in r.impacted_metrics
                    ],
                    "citations": [f"{c.id}: {c.title} ({c.year})" for c in r.citations],
                }
                for r in analysis_result.recommendations
            ],
            "literature_snippets": [
                {
                    "title": doc.title,
                    "snippet": doc.matched_snippet,
                    "citation": doc.citation.id,
                }
                for doc in analysis_result.retrieved_literature
            ],
        }

        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]

        # Add recent conversation history if provided
        if conversation_history:
            for turn in conversation_history[-4:]:
                messages.append(turn)

        messages.append(
            {
                "role": "user",
                "content": (
                    f"User Observation: '{user_message}'\n\n"
                    f"Ecological Diagnostic Analysis & Evidence Data:\n{context_data}\n\n"
                    "Please synthesize a scientific diagnosis and explain the evidence-backed recommendations."
                ),
            }
        )

        try:
            resp = httpx.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "https://darukaa.earth",
                    "X-Title": "Darukaa.Earth Biodiversity Intelligence",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 1200,
                },
                timeout=18.0,
            )

            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                if content:
                    return content

            logger.warning(
                f"OpenRouter API returned status {resp.status_code}: {resp.text}"
            )
        except Exception as e:
            logger.error(f"OpenRouter LLM call failed: {e}")

        # Fallback to deterministic summary if LLM call fails
        return self._build_deterministic_summary(analysis_result)

    def _build_deterministic_summary(self, result: ScientificAnalysisResult) -> str:
        reply_paragraphs = [
            "### 🔬 Scientific Agroecological Diagnostic",
            f"**Parcel Diagnosis**: {result.parcel_summary}",
            "",
            "**Connected Variables Analyzed**:",
        ]
        for var in result.variable_connections:
            reply_paragraphs.append(f"- {var}")

        reply_paragraphs.append("")
        reply_paragraphs.append(
            f"**Identified Vulnerabilities ({len(result.critical_vulnerabilities)})**:"
        )
        for vuln in result.critical_vulnerabilities:
            reply_paragraphs.append(f"- ⚠️ {vuln}")

        reply_paragraphs.append("")
        reply_paragraphs.append(
            f"We have generated **{len(result.recommendations)} evidence-backed intervention pathways** "
            "with quantified multi-metric impacts and authoritative citations (FAO, IPCC, IPBES)."
        )

        return "\n".join(reply_paragraphs)
