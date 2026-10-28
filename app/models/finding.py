from typing import Literal

from pydantic import BaseModel, ConfigDict

class finding(BaseModel):
    """A governance or cost-risk finding for one cloud resource."""
    model_config = ConfigDict(extra="forbid")

    rule_id: str
    severity: Literal["low", "medium", "high"]
    resource_id: str
    reason: str
    recommendation: str

