from fastapi import APIRouter, HTTPException, status
from app.collectors import MockCollector
from app.models import CloudResource

router = APIRouter(
    prefix="/api/resources",
    tags=["resources"],
)

@router.get("", response_model=list[CloudResource])
def list_resources() -> list[CloudResource]:
    """Return the validated mock cloud inventory."""

    collector = MockCollector()
    return collector.collect()

@router.get("/{resource_id:path}", response_model=CloudResource)
def get_resource(resource_id: str) -> CloudResource:
    """Return one cloud resource by its provider ID."""

    resources = MockCollector().collect()

    resource = next(
        (
            item
            for item in resources
            if item.id == resource_id
        ),
        None,
    )

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource '{resource_id}' was not found.",
        )

    return resource

# @router.get("")
# def list_resources() -> dict:
#     """Return cloud resources discovered by the Janitor."""

#     return {
#         "count": 2,
#         "resources": [
#             {
#                 "id": "i-demo123",
#                 "name": "dev-web-server",
#                 "cloud": "aws",
#                 "resource_type": "ec2_instance",
#                 "region": "us-east-1",
#                 "status": "stopped",
#                 "tags": {
#                     "environment": "development"
#                 },
#             },
#             {
#                 "id": "azure-disk-demo",
#                 "name": "test-unattached-disk",
#                 "cloud": "azure",
#                 "resource_type": "managed_disk",
#                 "region": "eastus",
#                 "status": "unattached",
#                 "tags": {},
#             },
#         ],
#     }
