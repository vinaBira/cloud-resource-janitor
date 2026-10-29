from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

class ResourceSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_resources: int = Field(ge=0)
    flagged_resources: int = Field(ge=0)
    aws_resources: int = Field(ge=0)
    azure_resources: int = Field(ge=0)
    estimated_reviewable_cost: float = Field(ge=0)

class ScanResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["completed"]
    scanned_at: datetime
    resources_scanned: int = Field(ge=0)
    findings_generated: int = Field(ge=0)
    summary: ResourceSummary