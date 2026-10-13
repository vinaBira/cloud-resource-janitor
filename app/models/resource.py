from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class CloudResource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    cloud:str = Field(min_length=1)
    resource_type: str = Field(min_length=1)
    region: str = Field(min_length=1)
    state: str = Field(min_length=1)
    tags: dict[str, str] = Field(default_factory=dict)
    created_at: datetime | None = Field(default=None)
    last_activity: datetime | None = Field(default=None)
    estimated_monthly_cost: float | None = Field(default=None, ge=0.0)