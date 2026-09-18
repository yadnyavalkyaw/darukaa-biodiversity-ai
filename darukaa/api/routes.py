"""FastAPI route handlers for Darukaa.Earth Biodiversity Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from darukaa.api.schemas import (
    AnalyzeRequest,
    ChatRequest,
    ChatResponse,
    CorrelationsResponse,
    KnowledgeQueryRequest,
    KnowledgeQueryResponse,
    SpatialLookupRequest,
)
from darukaa.dialogue import ClarificationEngine, ParameterExtractor, SessionStore
from darukaa.engine import (
    EcologicalCausalGraph,
    EnvironmentalReasoner,
    EnvironmentalState,
    ScientificAnalysisResult,
)
from darukaa.engine.llm_client import OpenRouterLLMClient
from darukaa.knowledge import KnowledgeRetriever
from darukaa.spatial import GeoSpatialContext, SpatialContextResolver

router = APIRouter(prefix="/api")

# Shared singletons for performance and memory state
session_store = SessionStore()
extractor = ParameterExtractor()
clarifier = ClarificationEngine()
causal_graph = EcologicalCausalGraph()
retriever = KnowledgeRetriever()
reasoner = EnvironmentalReasoner(causal_graph=causal_graph, retriever=retriever)
spatial_resolver = SpatialContextResolver()
llm_client = OpenRouterLLMClient()


@router.post("/chat", response_model=ChatResponse)
async def chat_turn(payload: ChatRequest) -> ChatResponse:
    """Multi-turn conversational reasoning endpoint with state memory and active clarification."""
    session = session_store.get_or_create(payload.session_id)

    # 1. Update from explicit metrics if provided (e.g. from UI sliders or forms)
    if payload.explicit_metrics:
        session.accumulated_state = extractor.update_state_from_dict(
            session.accumulated_state, payload.explicit_metrics
        )

    # 2. Extract metrics from conversation text
    session.accumulated_state, extracted_dict = extractor.extract_from_text(
        session.accumulated_state, payload.message
    )
    session.add_user_turn(payload.message, extracted_dict)

    # 3. Check completeness
    clarification = clarifier.evaluate_completeness(session.accumulated_state)

    if clarification.is_incomplete:
        # Input has insufficient dimensions (< 3 variables)
        session.add_assistant_turn(
            clarification.system_response, clarification.missing_variables
        )
        return ChatResponse(
            session_id=session.session_id,
            reply=clarification.system_response,
            is_clarification=True,
            active_variables_count=session.accumulated_state.count_active_variables(),
            accumulated_metrics=session.accumulated_state.model_dump(exclude_none=True),
            recommendations=[],
            retrieved_evidence=[],
            suggested_quick_replies=clarification.suggested_quick_replies,
        )

    # 4. Synthesize multi-variable scientific reasoning
    result = reasoner.analyze(session.accumulated_state)

    # Formulate rich conversational reply using LLM (if key provided) or deterministic scientific synthesis
    history = [{"role": t.role, "content": t.content} for t in session.turns]
    full_reply = llm_client.synthesize_conversational_response(
        payload.message, result, conversation_history=history
    )
    session.add_assistant_turn(full_reply)

    return ChatResponse(
        session_id=session.session_id,
        reply=full_reply,
        is_clarification=False,
        active_variables_count=result.active_variables_count,
        accumulated_metrics=session.accumulated_state.model_dump(exclude_none=True),
        recommendations=result.recommendations,
        retrieved_evidence=result.retrieved_literature,
        suggested_quick_replies=[
            "How do these interventions affect farm profitability?",
            "What if annual rainfall drops another 20%?",
            "What native pollinator species will return first?",
            "Reset session to start fresh",
        ],
    )


@router.post("/analyze", response_model=ScientificAnalysisResult)
async def analyze_structured(payload: AnalyzeRequest) -> ScientificAnalysisResult:
    """Direct structured diagnostic endpoint accepting JSON metrics."""
    state = EnvironmentalState()
    state = extractor.update_state_from_dict(state, payload.model_dump(exclude_none=True))

    if state.count_active_variables() < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least two environmental variables are required to generate multi-metric reasoning.",
        )

    return reasoner.analyze(state)


@router.post("/knowledge/query", response_model=KnowledgeQueryResponse)
async def query_knowledge_base(payload: KnowledgeQueryRequest) -> KnowledgeQueryResponse:
    """Direct RAG retrieval endpoint for inspecting indexed literature and citations."""
    results = retriever.query(
        payload.query,
        domain=payload.domain,
        top_k=payload.top_k,
    )
    return KnowledgeQueryResponse(
        query=payload.query,
        total_matched=len(results),
        results=results,
    )


@router.get("/metrics/correlations", response_model=CorrelationsResponse)
async def get_correlations() -> CorrelationsResponse:
    """Returns the ecological causal dependency graph and transfer formulas."""
    edges = causal_graph.edges
    return CorrelationsResponse(
        edges=edges,
        total_edges=len(edges),
    )


@router.post("/spatial/lookup", response_model=GeoSpatialContext)
async def spatial_lookup(payload: SpatialLookupRequest) -> GeoSpatialContext:
    """Resolves coordinates or region names into climate and soil baselines."""
    if payload.latitude is not None and payload.longitude is not None:
        return spatial_resolver.resolve_by_coordinates(
            payload.latitude, payload.longitude
        )
    if payload.region_name:
        res = spatial_resolver.resolve_by_text(payload.region_name)
        if res:
            return res

    # Fallback to default semi-arid profile
    return spatial_resolver.resolve_by_coordinates(32.0, 72.0)
