from datetime import datetime, timedelta, timezone

from app.models import CloudResource, finding

def _normalized_tags(resource: CloudResource) -> dict[str, str]:
    """
    Normalize the tags of a resource by converting all keys to lowercase and stripping whitespace.
    """
    return {
        str(key).strip().lower(): str(value).strip()
        for key, value in resource.tags.items()
    }

def _utc_datetime(value: datetime) -> datetime:
    """
    Convert a datetime object to UTC timezone.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)

def missing_owner_tag(resource: CloudResource, evaluation_time: datetime) -> finding | None:
    """
    Check if a resource is missing an owner tag.
    """
    del evaluation_time
    tags = _normalized_tags(resource)
    if tags.get("owner"):
        return None
    
    return finding(
        rule_id="missing-owner-tag",
        severity="medium",
        resource_id=resource.id,
        reason="Resource has no owner tag.",
        recommendation=(
            "Identify and tag the responsible team before considering cleanup. "
            "Any cleanup requires human approval."
        ),
    )

def missing_environment_tag(
    resource: CloudResource,
    evaluation_time: datetime,
) -> finding | None:
    del evaluation_time

    tags = _normalized_tags(resource)

    if tags.get("environment"):
        return None

    return finding(
        rule_id="missing-environment-tag",
        severity="low",
        resource_id=resource.id,
        reason="Resource has no environment tag.",
        recommendation=(
            "Determine whether this resource is production, development, or "
            "test before making lifecycle decisions. Any cleanup requires "
            "human approval."
        ),
    )

def unattached_volume(
    resource: CloudResource,
    evaluation_time: datetime,
) -> finding | None:
    del evaluation_time

    storage_types = {"ebs_volume", "managed_disk"}

    if (
        resource.resource_type.lower() not in storage_types
        or resource.state.lower() != "unattached"
    ):
        return None

    return finding(
        rule_id="unattached-volume",
        severity="high",
        resource_id=resource.id,
        reason="Storage resource is not attached to a virtual machine.",
        recommendation=(
            "Verify snapshots, dependencies, and retention requirements before "
            "considering removal. Any cleanup requires human approval."
        ),
    )

def stopped_instance(
    resource: CloudResource,
    evaluation_time: datetime,
) -> finding | None:
    del evaluation_time

    compute_types = {"ec2_instance", "virtual_machine"}
    stopped_states = {"stopped", "deallocated"}

    if (
        resource.resource_type.lower() not in compute_types
        or resource.state.lower() not in stopped_states
    ):
        return None

    return finding(
        rule_id="stopped-instance",
        severity="medium",
        resource_id=resource.id,
        reason="Virtual machine is currently stopped.",
        recommendation=(
            "Confirm whether the workload is still needed and review associated "
            "storage and IP costs. Any cleanup requires human approval."
        ),
    )

def inactive_resource(
    resource: CloudResource,
    evaluation_time: datetime,
) -> finding | None:
    inactive_days = 60
    if resource.last_activity is None:
        return finding(
            rule_id="inactive-resource",
            severity="medium",
            resource_id=resource.id,
            reason="Resource has no recorded recent activity.",
            recommendation=(
                "Verify monitoring data and application ownership before "
                "considering cleanup. Any cleanup requires human approval."
            ),
        )
    
    evaluation_time = _utc_datetime(evaluation_time)
    last_activity = _utc_datetime(resource.last_activity)
    inactivity_threshold = evaluation_time - timedelta(days=inactive_days)

    if last_activity >= inactivity_threshold:
        return None
    
    inactive_for = (evaluation_time - last_activity).days

    return finding(
        rule_id="inactive-resource",
        severity="medium",
        resource_id=resource.id,
        reason=(
            f"Resource has no recorded activity for approximately "
            f"{inactive_for} days."
        ),
        recommendation=(
            "Confirm activity using provider monitoring and verify with the "
            "resource owner. Any cleanup requires human approval."
        ),
    )

def production_protection(
    resource: CloudResource,
    evaluation_time: datetime,
) -> finding | None:
    del evaluation_time

    tags = _normalized_tags(resource)

    is_production = tags.get("environment", "").lower() == "production"
    is_protected = tags.get("protected", "").lower() == "true"

    if not is_production and not is_protected:
        return None

    return finding(
        rule_id="production-protection",
        severity="low",
        resource_id=resource.id,
        reason="Resource is categorized as production or explicitly protected.",
        recommendation=(
            "Exclude this resource from automated cleanup recommendations and "
            "require explicit owner approval before any change."
        ),
    )

