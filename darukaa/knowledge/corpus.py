"""Curated scientific corpus for the Darukaa.Earth retrievable knowledge layer."""

from __future__ import annotations

from pydantic import BaseModel, Field


class KnowledgeChunk(BaseModel):
    id: str
    citation_id: str
    domain: str
    subdomain: str
    tags: list[str]
    title: str
    content: str
    quantitative_metrics: dict[str, str] = Field(default_factory=dict)
    ecological_mechanisms: list[str] = Field(default_factory=list)


SCIENTIFIC_CORPUS: list[KnowledgeChunk] = [
    KnowledgeChunk(
        id="chunk-soil-soc-degradation",
        citation_id="FAO-2020-GSOC",
        domain="soil",
        subdomain="soil_organic_carbon",
        tags=["soil", "organic_carbon", "microbiome", "semi-arid", "degradation"],
        title="Soil Organic Carbon Depletion in Intensive Monocultures",
        content=(
            "In semi-arid and sub-humid croplands, conventional tillage and monoculture cropping rapidly deplete "
            "soil organic carbon (SOC) below critical thresholds (often <0.5%). When SOC drops below 1.0%, soil aggregate "
            "stability collapses, leading to surface crusting, high bulk density (>1.5 g/cm3), and dramatic loss of "
            "microbial biomass carbon (MBC). This directly reduces biological nitrogen fixation, halts mycorrhizal hyphal "
            "networks, and limits root penetration depth."
        ),
        quantitative_metrics={
            "critical_soc_threshold": "< 1.0% (severe degradation < 0.5%)",
            "microbial_biomass_loss": "40% - 65% reduction",
            "soil_bulk_density_increase": "+0.2 - 0.4 g/cm3",
        },
        ecological_mechanisms=[
            "Tillage exposes particulate organic matter to rapid microbial oxidation",
            "Lack of continuous root exudates starves arbuscular mycorrhizal fungi (AMF)",
            "Aggregate breakdown reduces macropore volume and infiltration rates",
        ],
    ),
    KnowledgeChunk(
        id="chunk-soil-water-retention-soc",
        citation_id="FAO-2021-RECARB",
        domain="soil",
        subdomain="moisture_retention",
        tags=["soil", "organic_carbon", "water_retention", "moisture", "drought"],
        title="Hydrological Benefits of Increasing Soil Organic Matter",
        content=(
            "Soil organic carbon functions as an internal biological sponge. According to FAO Recarbonizing Global Soils "
            "technical synthesis, every 1% absolute increase in topsoil organic carbon expands available water capacity (AWC) "
            "by 140 to 180 m3 per hectare (approximately 18,000 to 24,000 gallons per acre). This additional water buffering "
            "capacity prolongs soil moisture availability by 10 to 21 days during dry spells, preventing plant permanent wilting "
            "and maintaining active rhizosphere microbiome respiration even under semi-arid conditions."
        ),
        quantitative_metrics={
            "water_retention_gain": "+140 to 180 m3/ha per 1% SOC increase",
            "drought_window_extension": "+10 to 21 days of available moisture",
            "evaporative_loss_reduction": "25% - 40% when paired with residue mulch",
        },
        ecological_mechanisms=[
            "Humic substances absorb up to 20 times their dry weight in capillary water",
            "Stable macro-aggregates protect water against deep gravitational percolation and surface runoff",
        ],
    ),
    KnowledgeChunk(
        id="chunk-agroforestry-semi-arid",
        citation_id="IPCC-2019-SRCCL",
        domain="land_use",
        subdomain="agroforestry",
        tags=[
            "agroforestry",
            "semi-arid",
            "monoculture",
            "wheat",
            "faidherbia",
            "biodiversity",
        ],
        title="Agroforestry Systems in Semi-Arid Monoculture Landscapes",
        content=(
            "Converting degraded semi-arid monocultures (such as continuous wheat or barley) to multi-strata agroforestry "
            "utilizing reverse-phenology nitrogen-fixing trees (e.g., Faidherbia albida, Acacia senegal, or Leucaena leucocephala) "
            "fundamentally restores ecological balance. Faidherbia sheds leaves during the wet growing season, depositing "
            "20-40 kg N/ha into the topsoil and avoiding canopy shade competition with underlying crops, while providing shade and "
            "wind protection during hot post-harvest dry seasons. This practice increases soil organic carbon by 18-30% over 3-5 years "
            "and boosts crop resilience against drought by 20-35%."
        ),
        quantitative_metrics={
            "soc_increase_rate": "+0.15 - 0.35% absolute SOC over 3-5 years (18-30% relative)",
            "biological_n_fixation": "20 - 45 kg N/ha/year added to soil",
            "wind_erosion_reduction": "40% - 60% decrease in topsoil wind loss",
        },
        ecological_mechanisms=[
            "Reverse phenology avoids light competition during cereal crop growth",
            "Deep taproots (>15m) access subsoil moisture via hydraulic lift, rehydrating surface horizons",
            "Leaf litter enhances fungal-to-bacterial ratio and soil macrofauna (earthworms, beetles)",
        ],
    ),
    KnowledgeChunk(
        id="chunk-cover-crops-legumes",
        citation_id="FAO-2020-GSOC",
        domain="land_use",
        subdomain="cover_cropping",
        tags=["cover_crops", "legumes", "soil_carbon", "pollinators", "microbes"],
        title="Legume-Based Cover Cropping for Soil Regeneration and Pollinators",
        content=(
            "Integrating multi-species legume cover crops (e.g., Vicia villosa, Trifolium incarnatum, Cajanus cajan) during fallow "
            "periods or as intercrops increases topsoil organic carbon by 15-25% within 2 to 3 years. Legume roots host Rhizobium "
            "bacteria that fix 50 to 120 kg N/ha annually. Their prolonged blooming periods provide essential floral nectar and pollen "
            "sources, raising solitary bee and wild pollinator richness by 45-70%. Furthermore, diverse root exudates stimulate mycorrhizal "
            "glomalin production, which cements soil particles into erosion-resistant micro-aggregates."
        ),
        quantitative_metrics={
            "soc_gain_2_to_3_years": "+15% - 25% relative increase in topsoil SOC",
            "pollinator_richness_gain": "+45% - 70% increase in solitary bee/syrphid fly visits",
            "biological_n_fixation": "50 - 120 kg N/ha/year",
            "glomalin_production": "+30% - 55% increase in aggregate-stabilizing glomalin",
        },
        ecological_mechanisms=[
            "Continuous living roots sustain soil food webs during otherwise bare fallow seasons",
            "Floral continuity bridges the 'hunger gap' for native bees and parasitic wasps",
            "Low C:N ratio legume residues accelerate microbial mineralization and humification",
        ],
    ),
    KnowledgeChunk(
        id="chunk-biodiversity-insect-collapse",
        citation_id="IPBES-2019-GLOBAL",
        domain="biodiversity",
        subdomain="pollinators_insects",
        tags=["biodiversity", "pollinators", "fragmentation", "field_margins", "insects"],
        title="Mitigating Biodiversity Loss via Ecological Corridors and Field Margins",
        content=(
            "The IPBES Global Assessment highlights habitat fragmentation and monoculture uniformity as the primary causes of insect "
            "and pollinator collapse in working lands. Establishing native floral field margins (3-6 meter buffer strips of native perennials, "
            "wildflowers, and bunchgrasses) occupying just 5-8% of agricultural land area creates continuous ecological corridors. "
            "This intervention increases wild pollinator diversity by 50-80%, elevates natural predator arthropods (ladybugs, ground beetles, "
            "hoverflies) by 60%, and decreases pesticide requirements by 30-50% through biological pest regulation."
        ),
        quantitative_metrics={
            "wild_pollinator_diversity": "+50% - 80% species richness",
            "predatory_arthropod_abundance": "+60% higher natural enemy density",
            "pesticide_dependency_reduction": "30% - 50% reduction in synthetic spray needs",
        },
        ecological_mechanisms=[
            "Non-crop floral strips provide overwintering shelter, nesting cavities, and alternative prey",
            "Corridors facilitate gene flow between fragmented native habitat remnants",
            "Pest suppression operates via conservative biological control without toxic residues",
        ],
    ),
    KnowledgeChunk(
        id="chunk-soil-ph-nutrient-availability",
        citation_id="LAL-2004-SCIENCE",
        domain="soil",
        subdomain="soil_ph",
        tags=["soil", "ph", "acidity", "alkalinity", "mycorrhizae", "nutrients"],
        title="Soil pH Dynamics, Cation Exchange, and Rhizosphere Ecology",
        content=(
            "Soil pH is the master master variable governing biogeochemical cycles. At extreme pH (<5.2 or >8.3), phosphorus becomes "
            "chemically fixed (by aluminum/iron in acid soils, or calcium in alkaline soils), drastically limiting plant uptake. "
            "Highly acidic soils inhibit Rhizobium nodulation and earthworm viability. Incorporating organic amendments, biochar, or composted "
            "crop residues buffers soil pH toward the optimum range (6.2 - 7.3), increasing cation exchange capacity (CEC) by 25-40% "
            "and tripling beneficial rhizosphere bacterial counts."
        ),
        quantitative_metrics={
            "optimal_rhizosphere_ph": "6.2 to 7.3",
            "cec_improvement": "+25% - 40% with organic humates and biochar",
            "phosphorus_bioavailability": "+35% - 50% mobilization via mycorrhizal organic acids",
        },
        ecological_mechanisms=[
            "Humic acids possess high carboxyl and phenolic buffering capacity",
            "Neutralizing rhizosphere micro-zones promotes active nitrogenase enzyme activity",
        ],
    ),
    KnowledgeChunk(
        id="chunk-climate-buffering-microclimate",
        citation_id="IPCC-2022-WGII-CH5",
        domain="climate",
        subdomain="microclimate_regulation",
        tags=["climate", "temperature", "agroforestry", "thermal_stress", "resilience"],
        title="Microclimate Buffering and Thermal Dampening via Tree Canopies",
        content=(
            "Under accelerating global heating and erratic precipitation patterns, agroforestry systems with 15-30% canopy cover "
            "buffer extreme ambient temperatures, reducing understory ground surface temperatures by 2.0 to 4.5°C during summer heatwaves "
            "and reducing vapor pressure deficit (VPD) by 20-35%. This dampening effect preserves stomatal conductance in crops, "
            "prevents midday photosynthetic shutdown, and maintains high survival rates for juvenile ground-nesting pollinators and birds."
        ),
        quantitative_metrics={
            "surface_temperature_reduction": "2.0°C - 4.5°C cooler under canopy",
            "vpd_reduction": "20% - 35% lower atmospheric moisture stress",
            "crop_stomatal_conductance": "+25% - 40% sustained photosynthesis during heat peaks",
        },
        ecological_mechanisms=[
            "Canopy shade intercepts shortwave solar radiation and re-radiates longwave heat",
            "Tree transpiration produces localized evaporative cooling",
            "Windbreak effect lowers turbulent boundary layer heat exchange",
        ],
    ),
    KnowledgeChunk(
        id="chunk-human-impact-nitrogen-pollution",
        citation_id="SWIFT-2004-ECOSYS",
        domain="human_impact",
        subdomain="nutrient_pollution",
        tags=[
            "human_impact",
            "nitrogen",
            "runoff",
            "pollution",
            "eutrophication",
            "riparian",
        ],
        title="Mitigating Fertilizer Runoff and Restoring Aquatic-Terrestrial Ecotones",
        content=(
            "Excessive synthetic nitrogen application (>120 kg N/ha) in agricultural catchments leads to massive nitrate leaching "
            "into groundwater and surface water bodies, causing eutrophication and catastrophic freshwater biodiversity collapse. "
            "Implementing multi-tiered vegetated riparian buffers (native shrubs, deep-rooted willows/poplars, and perennial grasses) "
            "along field edges and watercourses intercepts 70-95% of dissolved nitrate runoff and 80% of particulate phosphorus through "
            "microbial denitrification and plant root uptake, while providing vital amphibian and macroinvertebrate habitat."
        ),
        quantitative_metrics={
            "nitrate_runoff_filtration": "70% - 95% nitrate removal efficiency",
            "sediment_phosphorus_trapping": "80% - 90% retention in 10m buffer zone",
            "aquatic_macroinvertebrate_index": "+65% diversity recovery within 3 years",
        },
        ecological_mechanisms=[
            "Saturated riparian root zones create anoxic micro-sites fueling denitrifying bacteria",
            "Perennial grass tussocks slow surface water velocity, dropping suspended sediment",
        ],
    ),
    KnowledgeChunk(
        id="chunk-biochar-recalcitrant-carbon",
        citation_id="PAUSTIAN-2016-NATURE",
        domain="soil",
        subdomain="biochar_amendment",
        tags=["biochar", "soil_carbon", "longevity", "microbiome", "cation_exchange"],
        title="Recalcitrant Soil Carbon Storage and Microbiome Catalysis via Biochar",
        content=(
            "Applying sustainably sourced pyrolysis biochar (applied at 10-15 tonnes/ha with compost inoculation) creates "
            "a highly porous, recalcitrant carbon matrix with a persistence half-life exceeding 200 years. The internal microscopic "
            "pore structure (micropores 2-50 nm) provides permanent refugia for mycorrhizal fungi and beneficial plant growth-promoting "
            "rhizobacteria (PGPR) shielding them from nematode predation. In sandy, degraded, or acidic soils, biochar application raises "
            "water holding capacity by 20-35% and increases soil microbial diversity (Shannon index) by 30%."
        ),
        quantitative_metrics={
            "carbon_permanence": ">200 years mean residence time",
            "microbial_shannon_diversity": "+30% - 45% increase in microbial richness",
            "water_holding_capacity": "+20% - 35% in coarse-textured soils",
        },
        ecological_mechanisms=[
            "High internal surface area (200-400 m2/g) adsorbs labile organic compounds and nutrients",
            "Pore size distribution protects bacterial colonies from protozoan grazing",
        ],
    ),
    KnowledgeChunk(
        id="chunk-monoculture-pest-vulnerability",
        citation_id="ALTIERI-1999-AGRO",
        domain="land_use",
        subdomain="crop_diversity",
        tags=["monoculture", "pest_dynamics", "intercropping", "predators", "diversity"],
        title="Trophic Collapse and Pest Outbreaks in Large-Scale Monocultures",
        content=(
            "Continuous cereal monocultures create severe ecological homogeneity, which eliminates natural biological checks. "
            "Specialist herbivorous pests thrive in monoculture expanses, while their natural insect predators (ladybird beetles, "
            "lacewings, parasitoid wasps) cannot survive due to the absence of continuous nectar sources, alternate prey, and overwintering "
            "substrates. Introducing strip intercropping (e.g., wheat intercropped with chickpeas or mustard) and flowering border strips "
            "restores multi-trophic regulation, lowering crop damage by 40-60% without requiring synthetic insecticides."
        ),
        quantitative_metrics={
            "herbivore_damage_reduction": "40% - 60% decrease in crop damage",
            "beneficial_parasitoid_density": "+3.2x increase over monoculture baseline",
            "yield_land_equivalent_ratio": "LER 1.18 to 1.35 (18-35% more land-efficient)",
        },
        ecological_mechanisms=[
            "Resource concentration hypothesis: specialized pests are disrupted by host plant camouflage and scent masking",
            "Enemies hypothesis: polycultures support higher populations of generalist and specialist natural enemies",
        ],
    ),
]
