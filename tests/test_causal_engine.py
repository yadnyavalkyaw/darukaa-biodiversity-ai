"""Tests for multi-metric causal reasoning and evidence synthesis."""

from darukaa.engine import (
    ClimateMetrics,
    EcologicalCausalGraph,
    EnvironmentalReasoner,
    EnvironmentalState,
    LandUseMetrics,
    SoilMetrics,
)


def test_causal_graph_initialization():
    graph = EcologicalCausalGraph()
    assert len(graph.edges) >= 7
    soc_edges = graph.get_edges_for_metric("soil_organic_carbon")
    assert len(soc_edges) >= 2


def test_benchmark_scenario_reasoning():
    """Validates the exact hackathon reference scenario:

    Input: SOC 0.3%, Rainfall low, Crop monoculture wheat, Region semi-arid.
    Expected: Multi-metric reasoning connecting >= 3 variables with FAO/IPCC citations.
    """
    state = EnvironmentalState(
        region_name="semi-arid",
        soil=SoilMetrics(organic_carbon_pct=0.3),
        climate=ClimateMetrics(rainfall_category="low", annual_rainfall_mm=320.0),
        land_use=LandUseMetrics(crop_system="monoculture wheat", land_type="cropland"),
    )

    reasoner = EnvironmentalReasoner()
    result = reasoner.analyze(state)

    # Validate active variables count >= 3
    assert result.active_variables_count >= 3
    assert len(result.critical_vulnerabilities) >= 2
    assert len(result.recommendations) >= 2

    # Validate agroforestry recommendation
    rec_agro = next(
        (r for r in result.recommendations if "Agroforestry" in r.title), None
    )
    assert rec_agro is not None
    assert "Faidherbia" in rec_agro.primary_action or "Acacia" in rec_agro.primary_action
    assert "reverse phenology" in rec_agro.scientific_reasoning.lower()
    assert len(rec_agro.connected_variables) >= 3

    # Check impacted metrics have quantitative forecasts
    soc_impact = next(
        (i for i in rec_agro.impacted_metrics if "Soil Organic Carbon" in i.metric_name),
        None,
    )
    assert soc_impact is not None
    assert "%" in soc_impact.projected_improvement

    water_impact = next(
        (i for i in rec_agro.impacted_metrics if "Water" in i.metric_name), None
    )
    assert water_impact is not None
    assert (
        "160" in water_impact.projected_improvement
        or "140" in water_impact.projected_improvement
    )

    # Check citations
    citation_ids = [c.id for c in rec_agro.citations]
    assert any("IPCC" in cid for cid in citation_ids)
    assert any("FAO" in cid for cid in citation_ids)


def test_acidic_soil_biochar_scenario():
    """Validates multi-variable reasoning for acidic soil with carbon depletion."""
    state = EnvironmentalState(
        soil=SoilMetrics(ph=5.2, organic_carbon_pct=0.7),
        land_use=LandUseMetrics(crop_system="continuous corn"),
    )
    reasoner = EnvironmentalReasoner()
    result = reasoner.analyze(state)

    biochar_rec = next((r for r in result.recommendations if "Biochar" in r.title), None)
    assert biochar_rec is not None
    assert any(
        "Cation Exchange Capacity" in i.metric_name for i in biochar_rec.impacted_metrics
    )
    assert biochar_rec.confidence_level >= 0.85
