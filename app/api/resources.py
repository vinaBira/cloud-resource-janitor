from fastapi import APIRouter
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
