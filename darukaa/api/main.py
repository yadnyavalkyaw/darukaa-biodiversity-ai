"""Main entrypoint for Darukaa.Earth AI Biodiversity Intelligence API."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from darukaa import __version__
from darukaa.api.routes import retriever
from darukaa.api.routes import router as api_router
from darukaa.api.schemas import ErrorDetail, HealthResponse, StandardErrorEnvelope

app = FastAPI(
    title="Darukaa.Earth AI Biodiversity Intelligence API",
    description="Scientific multi-metric causal reasoning and retrievable knowledge system for agroecological regeneration.",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for development and live deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Standardized validation error envelope adhering to production API standards."""
    details = []
    for err in exc.errors():
        field_name = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        details.append(ErrorDetail(field=field_name or None, issue=err["msg"]))

    envelope = StandardErrorEnvelope(
        code="VALIDATION_FAILED",
        message="Request payload failed schema validation.",
        details=details,
        timestamp=datetime.now(UTC).isoformat(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=envelope.model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches unhandled exceptions and masks internal stack traces in production."""
    envelope = StandardErrorEnvelope(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected internal server error occurred while processing ecological reasoning.",
        details=[ErrorDetail(field=None, issue=str(exc))],
        timestamp=datetime.now(UTC).isoformat(),
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=envelope.model_dump(),
    )


@app.get("/health", response_model=HealthResponse, tags=["Diagnostics"])
async def health_check() -> HealthResponse:
    """Health check and engine status."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        corpus_size=len(retriever.get_all_chunks()),
        timestamp=datetime.now(UTC).isoformat(),
    )


# Include API routes
app.include_router(api_router)

# Mount Static UI Files
ui_dir = Path(__file__).resolve().parent.parent / "ui"
if ui_dir.exists():
    app.mount("/", StaticFiles(directory=str(ui_dir), html=True), name="ui")
