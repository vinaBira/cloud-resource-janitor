from fastapi import APIRouter

from app.collectors import MockCollector
from app.models import ResourceSummary
from app.rules import evaluate_resources
from app.services import build_summary

router = APIRouter(
    prefix="/api/summary",
    tags=["summary"],
)


@router.get("", response_model=ResourceSummary)
def get_summary() -> ResourceSummary:
    """Return summarized cloud inventory and finding information."""

    resources = MockCollector().collect()
    findings = evaluate_resources(resources)

    return build_summary(
        resources=resources,
        findings=findings,
    )