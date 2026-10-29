from fastapi import APIRouter, Query
from typing import Literal

from app.collectors import MockCollector
from app.models import finding
from app.rules import evaluate_resources

router = APIRouter(
    prefix="/api/findings",
    tags=["findings"],
)

Severity = Literal["low", "medium", "high"]

@router.get("", response_model=list[finding])
def list_findings(
    severity: Severity | None = Query(
        default=None,
        description="Optionally filter findings by severity.",
    ),
) -> list[finding]:
    """Evaluate mock resources and return governance findings."""

    resources = MockCollector().collect()
    return evaluate_resources(resources)

    if severity is None:
        return findings

    return [
        finding
        for finding in findings
        if finding.severity == severity
    ]