"""Tests for spatial, biome, and coordinates lookup."""

from darukaa.spatial import SpatialContextResolver


def test_spatial_lookup_by_coordinates():
    resolver = SpatialContextResolver()
    # Coordinates in semi-arid region
    ctx = resolver.resolve_by_coordinates(32.0, 72.0)
    assert ctx.latitude == 32.0
    assert ctx.longitude == 72.0
    assert "Semi-Arid" in ctx.region_name or "Steppe" in ctx.region_name
    assert ctx.baseline_annual_rainfall_mm > 0
    assert len(ctx.typical_soil_orders) > 0


def test_spatial_lookup_by_text():
    resolver = SpatialContextResolver()
    ctx = resolver.resolve_by_text("Deccan Plateau Cotton")
    assert ctx is not None
    assert "Deccan" in ctx.region_name
    assert any("Vertisol" in s for s in ctx.typical_soil_orders)
