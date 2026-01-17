"""
Base repository with tenant-aware filtering.
All repositories inherit from TenantAwareRepository to enforce clinic_id isolation.
"""
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID


T = TypeVar('T')


class TenantAwareRepository(Generic[T]):
    """
    Base repository enforcing tenant isolation via clinic_id.
    
    All queries automatically filter by clinic_id to prevent cross-tenant data access.
    """
    
    def __init__(self, model: Type[T], session: Session):
        """
        Initialize repository with model and database session.
        
        Args:
            model: SQLAlchemy model class
            session: Database session
        """
        self.model = model
        self.session = session
    
    def get_by_id(self, id: UUID, clinic_id: UUID) -> Optional[T]:
        """
        Get a single record by ID with tenant filtering.
        
        Args:
            id: Record ID
            clinic_id: Clinic ID for tenant isolation
            
        Returns:
            Model instance or None if not found
        """
        stmt = select(self.model).where(
            self.model.id == id,
            self.model.clinic_id == clinic_id
        )
        return self.session.execute(stmt).scalar_one_or_none()
    
    def list(self, clinic_id: UUID, limit: Optional[int] = None, offset: Optional[int] = None) -> List[T]:
        """
        List all records for a clinic with optional pagination.
        
        Args:
            clinic_id: Clinic ID for tenant isolation
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model instances
        """
        stmt = select(self.model).where(self.model.clinic_id == clinic_id)
        
        if limit:
            stmt = stmt.limit(limit)
        if offset:
            stmt = stmt.offset(offset)
        
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def create(self, **kwargs) -> T:
        """
        Create a new record.
        
        Args:
            **kwargs: Model field values (must include clinic_id)
            
        Returns:
            Created model instance
            
        Raises:
            ValueError: If clinic_id not provided for tenant-scoped models
        """
        if hasattr(self.model, 'clinic_id') and 'clinic_id' not in kwargs:
            raise ValueError(f"clinic_id is required for {self.model.__name__}")
        
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def update(self, instance: T, **kwargs) -> T:
        """
        Update an existing record.
        
        Args:
            instance: Model instance to update
            **kwargs: Fields to update
            
        Returns:
            Updated model instance
        """
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def delete(self, instance: T) -> None:
        """
        Delete a record.
        
        Args:
            instance: Model instance to delete
        """
        self.session.delete(instance)
        self.session.commit()
