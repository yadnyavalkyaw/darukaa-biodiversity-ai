"""Pydantic v2 schemas for Darukaa.Earth REST API."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from darukaa.engine.causal_graph import CausalEdge
from darukaa.engine.reasoner import (
    RetrievedEvidence,
    ScientificRecommendation,
)


class ErrorDetail(BaseModel):
    field: str | None = None
    issue: str


class StandardErrorEnvelope(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=1, max_length=5000)
    session_id: str | None = None
    explicit_metrics: dict[str, Any] | None = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    is_clarification: bool
    active_variables_count: int
    accumulated_metrics: dict[str, Any]
    recommendations: list[ScientificRecommendation] = Field(default_factory=list)
    retrieved_evidence: list[RetrievedEvidence] = Field(default_factory=list)
    suggested_quick_replies: list[str] = Field(default_factory=list)


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    soil_organic_carbon_pct: float | None = Field(default=None, ge=0.0, le=20.0)
    soil_ph: float | None = Field(default=None, ge=3.0, le=11.0)
    soil_moisture_pct: float | None = Field(default=None, ge=0.0, le=100.0)
    annual_rainfall_mm: float | None = Field(default=None, ge=0.0)
    rainfall_category: str | None = None
    crop: str | None = None
    land_type: str | None = None
    synthetic_nitrogen_kg_ha: float | None = Field(default=None, ge=0.0)


class KnowledgeQueryRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    query: str = Field(min_length=2, max_length=500)
    domain: str | None = None
    top_k: int = Field(default=3, ge=1, le=10)


class KnowledgeQueryResponse(BaseModel):
    query: str
    total_matched: int
    results: list[RetrievedEvidence]


class CorrelationsResponse(BaseModel):
    edges: list[CausalEdge]
    total_edges: int


class SpatialLookupRequest(BaseModel):
    latitude: float | None = None
    longitude: float | None = None
    region_name: str | None = None


class HealthResponse(BaseModel):
    status: str
    version: str
    corpus_size: int
    timestamp: str
