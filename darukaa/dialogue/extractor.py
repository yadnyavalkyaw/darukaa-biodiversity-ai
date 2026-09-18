"""Parameter extraction engine for conversational text and structured JSON payloads."""

from __future__ import annotations

import re
from typing import Any

from darukaa.engine.metrics import (
    EnvironmentalState,
)
from darukaa.spatial.geocontext import SpatialContextResolver


class ParameterExtractor:
    """Extracts ecological parameters from unstructured conversation and structured dicts."""

    def __init__(self) -> None:
        self.spatial_resolver = SpatialContextResolver()

    def update_state_from_dict(
        self,
        current_state: EnvironmentalState,
        data: dict[str, Any],
    ) -> EnvironmentalState:
        """Merges structured key-value parameters into the accumulated environmental state."""
        # Top-level spatial
        if "region" in data or "region_name" in data:
            current_state.region_name = str(data.get("region") or data.get("region_name"))
        if "latitude" in data or "lat" in data:
            current_state.latitude = float(data.get("latitude") or data.get("lat"))
        if "longitude" in data or "lon" in data or "lng" in data:
            current_state.longitude = float(
                data.get("longitude") or data.get("lon") or data.get("lng")
            )

        # Soil parameters
        soc = (
            data.get("soil_organic_carbon")
            or data.get("soil_organic_carbon_pct")
            or data.get("soc")
        )
        if soc is not None:
            current_state.soil.organic_carbon_pct = float(
                str(soc).replace("%", "").strip()
            )

        ph = data.get("soil_ph") or data.get("ph")
        if ph is not None:
            current_state.soil.ph = float(ph)

        moisture = (
            data.get("soil_moisture")
            or data.get("soil_moisture_pct")
            or data.get("moisture")
        )
        if moisture is not None:
            current_state.soil.moisture_pct = float(
                str(moisture).replace("%", "").strip()
            )

        # Climate parameters
        rainfall = (
            data.get("annual_rainfall_mm")
            or data.get("rainfall_mm")
            or data.get("rainfall")
        )
        if rainfall is not None:
            try:
                current_state.climate.annual_rainfall_mm = float(
                    str(rainfall).replace("mm", "").strip()
                )
            except ValueError:
                # e.g. "low", "moderate", "high"
                current_state.climate.rainfall_category = str(rainfall).lower().strip()

        if "rainfall_category" in data:
            current_state.climate.rainfall_category = (
                str(data["rainfall_category"]).lower().strip()
            )

        # Land use parameters
        crop = data.get("crop") or data.get("crop_system") or data.get("cropping_system")
        if crop is not None:
            current_state.land_use.crop_system = str(crop).strip()

        land_type = data.get("land_type") or data.get("land_use")
        if land_type is not None:
            current_state.land_use.land_type = str(land_type).strip()

        # Human impact
        synth_n = (
            data.get("synthetic_nitrogen")
            or data.get("synthetic_nitrogen_kg_ha")
            or data.get("nitrogen_kg_ha")
        )
        if synth_n is not None:
            current_state.human_impact.synthetic_nitrogen_kg_ha = float(synth_n)

        # Spatial resolution if coordinates are provided
        if current_state.latitude is not None and current_state.longitude is not None:
            geo_ctx = self.spatial_resolver.resolve_by_coordinates(
                current_state.latitude, current_state.longitude
            )
            if not current_state.region_name:
                current_state.region_name = geo_ctx.region_name
            if current_state.climate.annual_rainfall_mm is None:
                current_state.climate.annual_rainfall_mm = (
                    geo_ctx.baseline_annual_rainfall_mm
                )

        return current_state

    def extract_from_text(
        self,
        current_state: EnvironmentalState,
        text: str,
    ) -> tuple[EnvironmentalState, dict[str, Any]]:
        """Parses conversational text for environmental metrics and updates state."""
        extracted: dict[str, Any] = {}
        cleaned = text.strip()

        # 1. Soil Organic Carbon extraction
        # Patterns like: "SOC: 0.3%", "soil organic carbon: 0.3%", "SOC 0.4", "carbon 0.3%", "0.3% soc"
        soc_match = re.search(
            r"(?:soc|soil\s+organic\s+carbon|carbon)\s*(?:is|:|=)?\s*([0-9]+(?:\.[0-9]+)?)\s*%",
            cleaned,
            re.IGNORECASE,
        )
        if not soc_match:
            soc_match = re.search(
                r"([0-9]+(?:\.[0-9]+)?)\s*%\s*(?:soc|soil\s+organic\s+carbon|carbon)",
                cleaned,
                re.IGNORECASE,
            )
        if not soc_match:
            soc_match = re.search(
                r"(?:soc|soil\s+organic\s+carbon)\s*(?:is|:|=)?\s*([0-9]+(?:\.[0-9]+)?)",
                cleaned,
                re.IGNORECASE,
            )
        if soc_match:
            val = float(soc_match.group(1))
            current_state.soil.organic_carbon_pct = val
            extracted["soil_organic_carbon_pct"] = val

        # 2. Soil pH extraction
        # e.g. "pH: 6.5", "pH 7.2", "pH is 5.8"
        ph_match = re.search(
            r"\bph\s*(?:is|:|=)?\s*([0-9]+(?:\.[0-9]+)?)\b", cleaned, re.IGNORECASE
        )
        if ph_match:
            val = float(ph_match.group(1))
            if 3.0 <= val <= 11.0:
                current_state.soil.ph = val
                extracted["soil_ph"] = val

        # 3. Rainfall / Precipitation extraction
        # e.g. "rainfall: low", "rainfall is low", "low rainfall", "350mm rainfall", "rainfall: 400 mm"
        rf_num_match = re.search(
            r"(?:rainfall|precipitation|rain)\s*(?:is|:|=)?\s*([0-9]+)\s*(?:mm)?\b",
            cleaned,
            re.IGNORECASE,
        )
        if not rf_num_match:
            rf_num_match = re.search(
                r"([0-9]+)\s*mm\s*(?:rainfall|rain|precipitation)?",
                cleaned,
                re.IGNORECASE,
            )

        if rf_num_match:
            val = float(rf_num_match.group(1))
            current_state.climate.annual_rainfall_mm = val
            extracted["annual_rainfall_mm"] = val
        else:
            rf_cat_match = re.search(
                r"(?:rainfall|precipitation)\s*(?:is|:|=)?\s*(low|moderate|medium|high|arid|dry)\b",
                cleaned,
                re.IGNORECASE,
            )
            if not rf_cat_match:
                rf_cat_match = re.search(
                    r"\b(low|moderate|medium|high|scarce)\s+(?:rainfall|rain|precipitation)\b",
                    cleaned,
                    re.IGNORECASE,
                )
            if rf_cat_match:
                cat = rf_cat_match.group(1).lower()
                cat = "low" if cat in ["low", "scarce", "dry", "arid"] else cat
                cat = "moderate" if cat in ["moderate", "medium"] else cat
                current_state.climate.rainfall_category = cat
                extracted["rainfall_category"] = cat

        # 4. Crop / Land Use extraction
        # e.g. "crop: monoculture wheat", "monoculture wheat", "wheat monoculture", "barley", "corn monoculture"
        crop_match = re.search(
            r"(?:crop|cropping\s+system)\s*(?:is|:|=)?\s*([a-zA-Z\s\-]+?)(?:\.|\n|,|$)",
            cleaned,
            re.IGNORECASE,
        )
        if crop_match:
            crop_val = crop_match.group(1).strip().lower()
            if (
                len(crop_val) > 2
                and "declining" not in crop_val
                and "biodiversity" not in crop_val
            ):
                current_state.land_use.crop_system = crop_val
                extracted["crop_system"] = crop_val
        elif (
            "monoculture wheat" in cleaned.lower()
            or "wheat monoculture" in cleaned.lower()
            or "wheat" in cleaned.lower()
            and "monoculture" in cleaned.lower()
        ):
            current_state.land_use.crop_system = "monoculture wheat"
            extracted["crop_system"] = "monoculture wheat"
        elif "monoculture" in cleaned.lower():
            current_state.land_use.crop_system = "monoculture"
            extracted["crop_system"] = "monoculture"

        # 5. Region / Ecoregion extraction
        region_match = re.search(
            r"(?:region|ecoregion|location|area)\s*(?:is|:|=)?\s*([a-zA-Z\s\-]+?)(?:\.|\n|,|$)",
            cleaned,
            re.IGNORECASE,
        )
        if region_match:
            r_val = region_match.group(1).strip().lower()
            if len(r_val) > 2 and "declining" not in r_val and "soil" not in r_val:
                current_state.region_name = r_val
                extracted["region_name"] = r_val
        elif "semi-arid" in cleaned.lower() or "semi arid" in cleaned.lower():
            current_state.region_name = "semi-arid"
            extracted["region_name"] = "semi-arid"
            if (
                not current_state.climate.rainfall_category
                and current_state.climate.annual_rainfall_mm is None
            ):
                current_state.climate.rainfall_category = "low"

        # 6. Coordinate extraction
        # e.g. "lat: 32.5, lon: 72.1" or "32.5, 72.1"
        coord_match = re.search(
            r"(?:lat|latitude)?\s*[:=]?\s*([-\d]+\.\d+)\s*,\s*(?:lon|longitude|lng)?\s*[:=]?\s*([-\d]+\.\d+)",
            cleaned,
            re.IGNORECASE,
        )
        if coord_match:
            lat = float(coord_match.group(1))
            lon = float(coord_match.group(2))
            current_state.latitude = lat
            current_state.longitude = lon
            extracted["latitude"] = lat
            extracted["longitude"] = lon
            geo_ctx = self.spatial_resolver.resolve_by_coordinates(lat, lon)
            if not current_state.region_name:
                current_state.region_name = geo_ctx.region_name
            if current_state.climate.annual_rainfall_mm is None:
                current_state.climate.annual_rainfall_mm = (
                    geo_ctx.baseline_annual_rainfall_mm
                )

        # 7. Synthetic Nitrogen extraction
        # e.g. "120 kg N/ha", "nitrogen: 150 kg/ha"
        n_match = re.search(
            r"(?:nitrogen|synthetic\s+n|fertilizer)\s*(?:is|:|=)?\s*([0-9]+)\s*(?:kg|kg\s*n/ha)?",
            cleaned,
            re.IGNORECASE,
        )
        if n_match:
            val = float(n_match.group(1))
            current_state.human_impact.synthetic_nitrogen_kg_ha = val
            extracted["synthetic_nitrogen_kg_ha"] = val

        return current_state, extracted
