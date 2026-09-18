"""Clarifying question generator for incomplete conversational inputs."""

from __future__ import annotations

from pydantic import BaseModel, Field

from darukaa.engine.metrics import EnvironmentalState


class ClarificationRequest(BaseModel):
    is_incomplete: bool
    missing_variables: list[str]
    system_response: str
    suggested_quick_replies: list[str] = Field(default_factory=list)


class ClarificationEngine:
    """Evaluates input completeness and formulates targeted scientific clarifying inquiries."""

    def evaluate_completeness(self, state: EnvironmentalState) -> ClarificationRequest:
        active_count = state.count_active_variables()
        missing: list[str] = []

        # Core required triage pillars
        has_soc = state.soil.organic_carbon_pct is not None
        has_rainfall = (
            state.climate.annual_rainfall_mm is not None
            or state.climate.rainfall_category is not None
        )
        has_land_or_crop = (
            state.land_use.crop_system is not None
            or state.land_use.land_type is not None
            or state.region_name is not None
        )

        if not has_soc:
            missing.append("soil_organic_carbon_pct")
        if not has_rainfall:
            missing.append("rainfall_pattern")
        if not has_land_or_crop:
            missing.append("land_use_type")

        # If at least 3 variables exist, we can proceed to full analysis
        if active_count >= 3 or len(missing) == 0:
            return ClarificationRequest(
                is_incomplete=False,
                missing_variables=[],
                system_response="",
                suggested_quick_replies=[],
            )

        # Build scientifically grounded clarifying response
        # Matches Hackathon example:
        # User: "Biodiversity is declining on my land"
        # System: "Can you provide soil organic carbon %, rainfall pattern, and land use type?"
        formatted_missing = []
        if not has_soc:
            formatted_missing.append("soil organic carbon %")
        if not has_rainfall:
            formatted_missing.append("rainfall pattern")
        if not has_land_or_crop:
            formatted_missing.append("land use type")

        if len(formatted_missing) == 3:
            msg = (
                "To formulate evidence-backed, non-obvious recommendations tailored to your ecosystem, "
                "I need a few critical diagnostic metrics:\n\n"
                "Can you provide **soil organic carbon %**, **rainfall pattern**, and **land use type**?\n\n"
                "*(Why this matters: Soil organic carbon governs water retention and mycorrhizal networks, "
                "rainfall dictates drought-resilient species selection, and land use identifies habitat fragmentation risks.)*"
            )
            quick_replies = [
                "SOC: 0.3%, Rainfall: Low, Crop: Monoculture wheat (Semi-arid)",
                "SOC: 0.8%, Rainfall: 600mm, Crop: Maize monoculture",
                "SOC: 1.5%, Rainfall: High (1100mm), Land: Pasture/Orchard",
                "I don't have soil tests; use semi-arid regional baselines",
            ]
        elif len(formatted_missing) == 2:
            items_str = " and ".join(formatted_missing)
            msg = (
                f"We have noted your initial ecological context. To accurately link soil-climate-biodiversity "
                f"feedbacks, could you also specify **{items_str}**?"
            )
            quick_replies = [
                "Rainfall is low (<400mm/yr)",
                "Soil organic carbon is approximately 0.4%",
                "Cropping system is monoculture wheat",
            ]
        else:
            item_str = formatted_missing[0]
            msg = (
                f"Almost there for a complete diagnostic! Could you please provide your **{item_str}** "
                f"so we can model the multi-metric causal pathways accurately?"
            )
            quick_replies = [
                "Low rainfall (<400mm)",
                "SOC: 0.5%",
                "Monoculture wheat",
            ]

        return ClarificationRequest(
            is_incomplete=True,
            missing_variables=missing,
            system_response=msg,
            suggested_quick_replies=quick_replies,
        )
