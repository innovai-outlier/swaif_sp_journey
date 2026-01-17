"""
ClinicMembership join table for Admin users with multiple clinic access.
"""
from sqlalchemy import Column, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.src.models.base import Base, BaseModel


class ClinicMembership(Base, BaseModel):
    """
    ClinicMembership join table linking Admin users to clinics.
    
    Enables admins to have access to multiple clinics.
    """
    __tablename__ = 'clinic_memberships'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    clinic_id = Column(UUID(as_uuid=True), ForeignKey('clinics.id', ondelete='CASCADE'), nullable=False, index=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'clinic_id', name='uq_user_clinic'),
    )
    
    # Relationships
    user = relationship('User', back_populates='clinic_memberships')
    clinic = relationship('Clinic', back_populates='users')
    
    def __repr__(self):
        return f"<ClinicMembership(user_id={self.user_id}, clinic_id={self.clinic_id})>"
