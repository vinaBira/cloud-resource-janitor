from collections.abc import Iterable
from app.models import CloudResource, finding, ResourceSummary 

NON_ACTIONABLE_RULES = {
    "production-protection",
}

def build_summary(
    resources: Iterable[CloudResource],
    findings: Iterable[Finding],
) -> ResourceSummary:
    """Build an inventory and reviewable-cost summary."""

    resource_list = list(resources)
    finding_list = list(findings)

    actionable_resource_ids = {
        finding.resource_id
        for finding in finding_list
        if finding.rule_id not in NON_ACTIONABLE_RULES
    }

    reviewable_cost = sum(
        resource.estimated_monthly_cost or 0
        for resource in resource_list
        if resource.id in actionable_resource_ids
    )

    return ResourceSummary(
        total_resources=len(resource_list),
        flagged_resources=len(actionable_resource_ids),
        aws_resources=sum(
            1
            for resource in resource_list
            if resource.cloud.lower() == "aws"
        ),
        azure_resources=sum(
            1
            for resource in resource_list
            if resource.cloud.lower() == "azure"
        ),
        estimated_reviewable_cost=round(reviewable_cost, 2),
    )