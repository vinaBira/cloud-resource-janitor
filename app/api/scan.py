from datetime import datetime, timezone

from fastapi import APIRouter

from app.collectors import MockCollector
from app.models import ScanResult
from app.rules import evaluate_resources
from app.services import build_summary

router = APIRouter(
    prefix="/api/scan",
    tags=["scan"],
)


@router.post("", response_model=ScanResult)
def run_scan() -> ScanResult:
    """Run a read-only inventory scan and rule evaluation."""

    scanned_at = datetime.now(timezone.utc)
    resources = MockCollector().collect()

    findings = evaluate_resources(
        resources=resources,
        evaluation_time=scanned_at,
    )

    summary = build_summary(
        resources=resources,
        findings=findings,
    )

    return ScanResult(
        status="completed",
        scanned_at=scanned_at,
        resources_scanned=len(resources),
        findings_generated=len(findings),
        summary=summary,
    )