"""
Base Pydantic schemas for request/response models.
Provides common schema patterns and utilities.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class BaseSchema(BaseModel):
    """
    Base schema with common configuration.
    """
    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    """
    Schema mixin for models with timestamps.
    """
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Record last update timestamp")


class IDSchema(BaseSchema):
    """
    Schema mixin for models with UUID identifier.
    """
    id: UUID = Field(..., description="Unique identifier")


class BaseResponse(IDSchema, TimestampSchema):
    """
    Base response schema with ID and timestamps.
    """
    pass
