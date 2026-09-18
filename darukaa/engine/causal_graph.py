"""Ecological Causal Graph and Multi-Metric Interactions for Darukaa.Earth.

Encodes biogeochemical dependencies, ecological transfer functions, and multi-variable
feedback loops connecting soil, climate, land use, biodiversity, and human impact.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CausalEdge(BaseModel):
    source_metric: str
    target_metric: str
    interaction_type: str = Field(
        description="positive_feedback, negative_feedback, threshold_collapse, synergistic"
    )
    strength: float = Field(ge=0.0, le=1.0)
    scientific_mechanism: str
    governing_equation_or_rule: str
    citation_id: str


class EcologicalCausalGraph:
    """Directed graph representing verified ecological interconnections."""

    def __init__(self) -> None:
        self.edges: list[CausalEdge] = self._init_edges()

    def _init_edges(self) -> list[CausalEdge]:
        return [
            CausalEdge(
                source_metric="soil_organic_carbon",
                target_metric="available_water_capacity",
                interaction_type="synergistic",
                strength=0.95,
                scientific_mechanism=(
                    "Humic substances and particulate organic matter act as biological sponges, "
                    "expanding soil pore space and capillary moisture retention capacity."
                ),
                governing_equation_or_rule="ΔAWC = ΔSOC% × 160 m3/ha (+18,000 to 24,000 gal/acre per 1% SOC)",
                citation_id="FAO-2021-RECARB",
            ),
            CausalEdge(
                source_metric="soil_organic_carbon",
                target_metric="microbial_biomass_carbon",
                interaction_type="positive_feedback",
                strength=0.90,
                scientific_mechanism=(
                    "SOC provides the labile carbon substrates and energy needed for bacteria, mycorrhizal fungi, "
                    "and actinomycetes to build stable micro-aggregates via glomalin secretion."
                ),
                governing_equation_or_rule="Microbial Biomass Carbon ≈ 2.5% to 4.0% of Total SOC Pool",
                citation_id="FAO-2020-GSOC",
            ),
            CausalEdge(
                source_metric="crop_system_monoculture",
                target_metric="wild_pollinator_richness",
                interaction_type="threshold_collapse",
                strength=0.88,
                scientific_mechanism=(
                    "Extensive monocultures create floral resource deserts outside brief blooming windows, "
                    "eliminating solitary bee nesting sites and starvation refugia."
                ),
                governing_equation_or_rule="Pollinator diversity drops by 50-75% when floral continuity < 4 months/yr",
                citation_id="IPBES-2019-GLOBAL",
            ),
            CausalEdge(
                source_metric="annual_rainfall_low",
                target_metric="topsoil_wind_erosion",
                interaction_type="synergistic",
                strength=0.85,
                scientific_mechanism=(
                    "In arid and semi-arid environments (<400mm), low moisture coupled with bare soil or "
                    "post-harvest wheat stubble removal leaves fine soil particles vulnerable to saltation and deflation."
                ),
                governing_equation_or_rule="Wind erosion rate increases exponentially when SOC < 0.8% and canopy cover < 10%",
                citation_id="IPCC-2019-SRCCL",
            ),
            CausalEdge(
                source_metric="agroforestry_canopy_cover",
                target_metric="understory_microclimate_temperature",
                interaction_type="negative_feedback",
                strength=0.87,
                scientific_mechanism=(
                    "Tree canopies intercept shortwave solar irradiance and transpire moisture, creating "
                    "localized microclimate dampening that lowers maximum understory surface temperatures."
                ),
                governing_equation_or_rule="ΔT_surface = -2.0°C to -4.5°C when woody canopy is between 15% and 30%",
                citation_id="IPCC-2022-WGII-CH5",
            ),
            CausalEdge(
                source_metric="legume_cover_crops",
                target_metric="biological_nitrogen_fixation",
                interaction_type="positive_feedback",
                strength=0.92,
                scientific_mechanism=(
                    "Symbiotic Rhizobium root nodulation fixes atmospheric N2 into plant-available NH4+, "
                    "reducing dependence on synthetic nitrogen and preventing groundwater leaching."
                ),
                governing_equation_or_rule="Biological N Fixation = 50 to 120 kg N/ha/season",
                citation_id="SWIFT-2004-ECOSYS",
            ),
            CausalEdge(
                source_metric="habitat_fragmentation",
                target_metric="predatory_arthropod_suppression",
                interaction_type="negative_feedback",
                strength=0.82,
                scientific_mechanism=(
                    "Lack of continuous hedgerows or field margins limits dispersal corridors for carabid ground "
                    "beetles and spiders, allowing pest insect flare-ups."
                ),
                governing_equation_or_rule="Natural pest control efficiency decreases by 40% with every 200m distance from margin",
                citation_id="ALTIERI-1999-AGRO",
            ),
            CausalEdge(
                source_metric="biochar_amendment",
                target_metric="soil_cation_exchange_capacity",
                interaction_type="synergistic",
                strength=0.89,
                scientific_mechanism=(
                    "High surface area and oxygenated functional groups (carboxyl, hydroxyl) on pyrolyzed biochar "
                    "particles retain Ca2+, Mg2+, and K+ ions, preventing nutrient leaching in sandy or degraded soils."
                ),
                governing_equation_or_rule="ΔCEC = +20% to +40% with 10-15 t/ha biochar + compost blend",
                citation_id="PAUSTIAN-2016-NATURE",
            ),
        ]

    def get_edges_for_metric(self, metric_name: str) -> list[CausalEdge]:
        return [
            e
            for e in self.edges
            if metric_name in e.source_metric or metric_name in e.target_metric
        ]

    def get_all_edges_dict(self) -> list[dict[str, Any]]:
        return [e.model_dump() for e in self.edges]
