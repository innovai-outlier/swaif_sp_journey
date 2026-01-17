"""
Base database model with common fields and utilities.
All models inherit from Base to get SQLAlchemy ORM features.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid


Base = declarative_base()


class BaseModel:
    """
    Base mixin providing common fields for all models.
    
    Fields:
        id: UUID primary key
        created_at: Timestamp of record creation
        updated_at: Timestamp of last update
    """
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
