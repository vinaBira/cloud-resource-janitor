from collections.abc import Callable, Iterable
from datetime import datetime, timezone

from app.models import CloudResource, finding
from app.rules.resource_rules import (
    inactive_resource,
    missing_environment_tag,
    missing_owner_tag,
    unattached_volume,
    stopped_instance,
    production_protection
)

Rule = Callable[[CloudResource, datetime], finding | None]

RULES: tuple[Rule, ...] = (
    missing_owner_tag,
    missing_environment_tag,
    unattached_volume,
    stopped_instance,
    inactive_resource,
    production_protection,
)

def evaluate_resource(
    resource: CloudResource,
    evaluation_time: datetime,
) -> list[finding]:
    """Run every registered rule against one resource."""

    findings: list[finding] = []

    for rule in RULES:
        finding = rule(resource, evaluation_time)

        if finding is not None:
            findings.append(finding)

    return findings


def evaluate_resources(
    resources: Iterable[CloudResource],
    evaluation_time: datetime | None = None,
) -> list[finding]:
    """Run all rules against all supplied resources."""

    effective_time = evaluation_time or datetime.now(timezone.utc)
    findings: list[finding] = []

    for resource in resources:
        findings.extend(
            evaluate_resource(
                resource=resource,
                evaluation_time=effective_time,
            )
        )

    return findings