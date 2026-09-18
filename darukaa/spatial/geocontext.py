"""Geo-spatial and Biome Context Resolver for Darukaa.Earth.

Translates geographic coordinates (latitude, longitude) or named ecoregions into
Köppen-Geiger climate zones, typical soil orders, native vegetation reference biomes,
and baseline environmental metrics.
"""

from __future__ import annotations

from pydantic import BaseModel


class GeoSpatialContext(BaseModel):
    region_name: str
    latitude: float | None = None
    longitude: float | None = None
    koppen_climate_zone: str
    climate_classification: str
    baseline_annual_rainfall_mm: float
    typical_soil_orders: list[str]
    reference_native_biome: str
    dominant_ecological_risks: list[str]
    typical_baseline_soc_pct: float


# Curated spatial ecoregions covering major global agricultural and semi-arid landscapes
ECOREGION_DATABASE: list[GeoSpatialContext] = [
    GeoSpatialContext(
        region_name="Semi-Arid Drylands / Steppe",
        latitude=32.0,
        longitude=72.0,
        koppen_climate_zone="BSh / BSk",
        climate_classification="Arid / Semi-Arid Steppe",
        baseline_annual_rainfall_mm=350.0,
        typical_soil_orders=["Aridisols", "Vertisols", "Calcisols"],
        reference_native_biome="Temperate Grasslands, Savannas & Shrublands",
        dominant_ecological_risks=[
            "Wind erosion",
            "Soil crusting",
            "Acute drought deficit",
            "Soil carbon depletion",
        ],
        typical_baseline_soc_pct=0.45,
    ),
    GeoSpatialContext(
        region_name="Deccan Plateau Semi-Arid",
        latitude=17.5,
        longitude=76.0,
        koppen_climate_zone="BSh",
        climate_classification="Hot Semi-Arid",
        baseline_annual_rainfall_mm=620.0,
        typical_soil_orders=[
            "Vertisols (Black Cotton Soil)",
            "Alfisols (Red Sandy Loam)",
        ],
        reference_native_biome="Tropical Dry Deciduous Forest & Thorny Scrub",
        dominant_ecological_risks=[
            "Groundwater over-extraction",
            "High soil clay shrink-swell crack erosion",
            "Monoculture cotton/cereal vulnerability",
        ],
        typical_baseline_soc_pct=0.55,
    ),
    GeoSpatialContext(
        region_name="Indo-Gangetic Plain",
        latitude=28.5,
        longitude=77.2,
        koppen_climate_zone="Cwa",
        climate_classification="Monsoon-influenced Humid Subtropical",
        baseline_annual_rainfall_mm=750.0,
        typical_soil_orders=["Inceptisols", "Entisols (Alluvial Deep Silt)"],
        reference_native_biome="Terrestrial Floodplain Moist & Dry Forest",
        dominant_ecological_risks=[
            "Intensive synthetic fertilizer runoff",
            "Paddy stubble burning emission",
            "Falling water table",
            "Pesticide persistence",
        ],
        typical_baseline_soc_pct=0.65,
    ),
    GeoSpatialContext(
        region_name="Mediterranean Basin",
        latitude=38.0,
        longitude=14.0,
        koppen_climate_zone="Csa",
        climate_classification="Hot-summer Mediterranean",
        baseline_annual_rainfall_mm=520.0,
        typical_soil_orders=["Alfisol (Terra Rossa)", "Inceptisols"],
        reference_native_biome="Mediterranean Forests, Woodlands & Scrub",
        dominant_ecological_risks=[
            "Summer drought",
            "Wildfire risk",
            "Steep slope water erosion",
            "Olive/vineyard bare soil desiccation",
        ],
        typical_baseline_soc_pct=0.85,
    ),
    GeoSpatialContext(
        region_name="Sub-Saharan Sahelian Belt",
        latitude=14.0,
        longitude=2.0,
        koppen_climate_zone="BSh",
        climate_classification="Dry Tropical Semi-Arid",
        baseline_annual_rainfall_mm=380.0,
        typical_soil_orders=["Arenosols", "Lixisols"],
        reference_native_biome="Sahelian Acacia Savanna",
        dominant_ecological_risks=[
            "Desertification",
            "Severe topsoil stripping",
            "Nutrient-poor sandy texture",
            "Termite and livestock pressure",
        ],
        typical_baseline_soc_pct=0.30,
    ),
    GeoSpatialContext(
        region_name="Temperate Grain Belt (North America / Eurasian Steppe)",
        latitude=45.0,
        longitude=-95.0,
        koppen_climate_zone="Dfb / BSk",
        climate_classification="Humid Continental / Dry Steppe",
        baseline_annual_rainfall_mm=680.0,
        typical_soil_orders=["Mollisols (High Organic Prairie Soils)"],
        reference_native_biome="Tallgrass / Mixed-grass Prairie",
        dominant_ecological_risks=[
            "Deep tillage compaction",
            "Tile drainage nutrient runoff into waterways",
            "Loss of prairie pothole wetlands",
        ],
        typical_baseline_soc_pct=1.80,
    ),
]


class SpatialContextResolver:
    """Resolves spatial queries via coordinates or descriptive location names."""

    def resolve_by_coordinates(self, lat: float, lon: float) -> GeoSpatialContext:
        """Finds closest ecoregion profile based on Euclidean coordinate distance."""
        best_match = ECOREGION_DATABASE[0]
        min_dist_sq = float("inf")

        for eco in ECOREGION_DATABASE:
            if eco.latitude is None or eco.longitude is None:
                continue
            dist_sq = (lat - eco.latitude) ** 2 + (lon - eco.longitude) ** 2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                best_match = eco

        # Return clone with exact query coordinates
        return GeoSpatialContext(
            region_name=best_match.region_name,
            latitude=lat,
            longitude=lon,
            koppen_climate_zone=best_match.koppen_climate_zone,
            climate_classification=best_match.climate_classification,
            baseline_annual_rainfall_mm=best_match.baseline_annual_rainfall_mm,
            typical_soil_orders=best_match.typical_soil_orders,
            reference_native_biome=best_match.reference_native_biome,
            dominant_ecological_risks=best_match.dominant_ecological_risks,
            typical_baseline_soc_pct=best_match.typical_baseline_soc_pct,
        )

    def resolve_by_text(self, text: str) -> GeoSpatialContext | None:
        """Searches ecoregion database by text keywords."""
        query_lower = text.lower()
        for eco in ECOREGION_DATABASE:
            if (
                eco.region_name.lower() in query_lower
                or any(
                    risk.lower() in query_lower for risk in eco.dominant_ecological_risks
                )
                or any(soil.lower() in query_lower for soil in eco.typical_soil_orders)
            ):
                return eco

        # Keyword heuristics
        if (
            "semi-arid" in query_lower
            or "dryland" in query_lower
            or "steppe" in query_lower
        ):
            return ECOREGION_DATABASE[0]
        if "india" in query_lower or "deccan" in query_lower or "cotton" in query_lower:
            return ECOREGION_DATABASE[1]
        if "ganga" in query_lower or "punjab" in query_lower or "plain" in query_lower:
            return ECOREGION_DATABASE[2]
        if (
            "mediterranean" in query_lower
            or "olive" in query_lower
            or "italy" in query_lower
            or "spain" in query_lower
        ):
            return ECOREGION_DATABASE[3]
        if "sahel" in query_lower or "africa" in query_lower:
            return ECOREGION_DATABASE[4]

        return None
