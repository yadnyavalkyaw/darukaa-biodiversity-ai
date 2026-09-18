"""Pydantic v2 schemas and models for environmental metrics and indicators."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field, model_validator


class MetricHealthStatus(StrEnum):
    OPTIMAL = "optimal"
    MODERATE = "moderate"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class SoilMetrics(BaseModel):
    organic_carbon_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=20.0,
        description="Soil Organic Carbon percentage (0-20%)",
    )
    ph: float | None = Field(
        default=None,
        ge=3.0,
        le=11.0,
        description="Soil pH (3-11)",
    )
    moisture_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Soil volumetric water content %",
    )
    bulk_density_g_cm3: float | None = Field(
        default=None,
        ge=0.5,
        le=2.2,
        description="Dry bulk density in g/cm3",
    )
    nitrogen_ppm: float | None = Field(
        default=None,
        ge=0.0,
        description="Available mineral nitrogen in parts per million",
    )

    def evaluate_soc_status(self) -> MetricHealthStatus:
        if self.organic_carbon_pct is None:
            return MetricHealthStatus.UNKNOWN
        if self.organic_carbon_pct < 0.6:
            return MetricHealthStatus.CRITICAL
        if self.organic_carbon_pct < 1.2:
            return MetricHealthStatus.DEGRADED
        if self.organic_carbon_pct < 2.5:
            return MetricHealthStatus.MODERATE
        return MetricHealthStatus.OPTIMAL

    def evaluate_ph_status(self) -> MetricHealthStatus:
        if self.ph is None:
            return MetricHealthStatus.UNKNOWN
        if 6.2 <= self.ph <= 7.4:
            return MetricHealthStatus.OPTIMAL
        if (5.5 <= self.ph < 6.2) or (7.4 < self.ph <= 8.2):
            return MetricHealthStatus.MODERATE
        return MetricHealthStatus.DEGRADED


class ClimateMetrics(BaseModel):
    annual_rainfall_mm: float | None = Field(
        default=None,
        ge=0.0,
        le=10000.0,
        description="Mean annual precipitation in mm",
    )
    rainfall_category: str | None = Field(
        default=None,
        description="low (<400mm), moderate (400-800mm), high (>800mm)",
    )
    aridity_index: float | None = Field(
        default=None,
        description="UNEP Aridity Index (P/PET). Semi-arid is 0.20-0.50, Arid < 0.20",
    )
    mean_temperature_c: float | None = Field(
        default=None,
        description="Mean annual temperature in degrees Celsius",
    )
    summer_peak_temp_c: float | None = Field(
        default=None,
        description="Maximum peak summer temperature in Celsius",
    )

    @model_validator(mode="after")
    def infer_rainfall_category(self) -> ClimateMetrics:
        if self.annual_rainfall_mm is not None and not self.rainfall_category:
            if self.annual_rainfall_mm < 400:
                self.rainfall_category = "low"
            elif self.annual_rainfall_mm <= 850:
                self.rainfall_category = "moderate"
            else:
                self.rainfall_category = "high"
        return self


class LandUseMetrics(BaseModel):
    land_type: str | None = Field(
        default=None,
        description="e.g. cropland, orchard, pasture, degraded fallow, semi-arid dryland",
    )
    crop_system: str | None = Field(
        default=None,
        description="e.g. monoculture wheat, maize-soy rotation, agroforestry, polyculture",
    )
    canopy_cover_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Tree/shrub woody canopy cover %",
    )
    slope_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Topographic slope percentage",
    )
    tillage_practice: str | None = Field(
        default=None,
        description="conventional, reduced_till, no_till",
    )
    fragmentation_level: str | None = Field(
        default=None,
        description="high, medium, low",
    )


class BiodiversityMetrics(BaseModel):
    species_richness: int | None = Field(
        default=None,
        description="Count of distinct plant/animal species observed",
    )
    pollinator_index: str | None = Field(
        default=None,
        description="high, moderate, low, collapsed",
    )
    soil_microbial_status: str | None = Field(
        default=None,
        description="active, suppressed, depleted",
    )
    native_vegetation_pct: float | None = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Percentage of native perennial flora",
    )


class HumanImpactMetrics(BaseModel):
    synthetic_nitrogen_kg_ha: float | None = Field(
        default=None,
        ge=0.0,
        description="Annual synthetic nitrogen fertilizer applied in kg N/ha",
    )
    pesticide_frequency_per_year: int | None = Field(
        default=None,
        ge=0,
        description="Chemical pesticide/fungicide spray applications per year",
    )
    deforestation_proximity_km: float | None = Field(
        default=None,
        ge=0.0,
        description="Distance to recent deforestation or land clearance edge",
    )


class EnvironmentalState(BaseModel):
    """Holistic representation of a land parcel's ecological conditions."""

    region_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    soil: SoilMetrics = Field(default_factory=SoilMetrics)
    climate: ClimateMetrics = Field(default_factory=ClimateMetrics)
    land_use: LandUseMetrics = Field(default_factory=LandUseMetrics)
    biodiversity: BiodiversityMetrics = Field(default_factory=BiodiversityMetrics)
    human_impact: HumanImpactMetrics = Field(default_factory=HumanImpactMetrics)

    def count_active_variables(self) -> int:
        """Counts how many key environmental variables have defined observations."""
        count = 0
        if self.soil.organic_carbon_pct is not None:
            count += 1
        if self.soil.ph is not None:
            count += 1
        if self.soil.moisture_pct is not None:
            count += 1
        if (
            self.climate.annual_rainfall_mm is not None
            or self.climate.rainfall_category is not None
        ):
            count += 1
        if (
            self.climate.mean_temperature_c is not None
            or self.climate.summer_peak_temp_c is not None
        ):
            count += 1
        if self.land_use.crop_system is not None:
            count += 1
        if self.land_use.land_type is not None or self.region_name is not None:
            count += 1
        if (
            self.biodiversity.pollinator_index is not None
            or self.biodiversity.species_richness is not None
        ):
            count += 1
        if (
            self.human_impact.synthetic_nitrogen_kg_ha is not None
            or self.human_impact.pesticide_frequency_per_year is not None
        ):
            count += 1
        return count
