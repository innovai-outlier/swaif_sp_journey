"""
Clinic model representing a medical clinic (tenant).
"""
from sqlalchemy import Column, String, Boolean, Integer, CheckConstraint
from sqlalchemy.orm import relationship
from backend.src.models.base import Base, BaseModel


class Clinic(Base, BaseModel):
    """
    Clinic entity for multi-tenant support.
    
    Each clinic is isolated from other clinics' data.
    """
    __tablename__ = 'clinics'
    
    name = Column(String(255), unique=True, nullable=False, index=True)
    is_training = Column(Boolean, nullable=False, default=False)
    analytics_period_days = Column(
        Integer,
        nullable=False,
        default=30
    )
    
    # Add constraint for analytics period range (7-90 days)
    __table_args__ = (
        CheckConstraint(
            'analytics_period_days >= 7 AND analytics_period_days <= 90',
            name='check_analytics_period_range'
        ),
    )
    
    # Relationships
    users = relationship('ClinicMembership', back_populates='clinic')
    methodologies = relationship('Methodology', back_populates='clinic')
    follow_up_plans = relationship('FollowUpPlan', back_populates='clinic')
    journey_stages = relationship('JourneyStage', back_populates='clinic')
    patients = relationship('Patient', back_populates='clinic')
    vendors = relationship('Vendor', back_populates='clinic')
    rewards = relationship('Reward', back_populates='clinic')
    
    def __repr__(self):
        return f"<Clinic(id={self.id}, name='{self.name}', is_training={self.is_training})>"
