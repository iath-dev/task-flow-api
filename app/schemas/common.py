from datetime import datetime
from pydantic import BaseModel, Field


class IdSchema(BaseModel):
    """Base schema for model with an ID"""

    id: int = Field(..., description="Unique identifier for the resource.")


class TimestampBase(BaseModel):
    """Base schema for models with creation and update timestampsHay forma"""

    created_at: datetime = Field(
        ..., description="Timestamp when the resource was created."
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the resource was last updated"
    )
