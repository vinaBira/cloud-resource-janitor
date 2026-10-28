from fastapi import APIRouter

from app.collectors import MockCollector
from app.models import finding
from app.rules import evaluate_resources

router = APIRouter(
    prefix="/api/findings",
    tags=["findings"],
)

@router.get("", response_model=list[finding])
def list_findings() -> list[finding]:
    """Evaluate mock resources and return governance findings."""

    resources = MockCollector().collect()
    return evaluate_resources(resources)