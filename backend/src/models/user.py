"""
User model for authentication (Clinic Admins and Patients).
"""
from sqlalchemy import Column, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from backend.src.models.base import Base, BaseModel
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "ADMIN"
    PATIENT = "PATIENT"


class User(Base, BaseModel):
    """
    User entity for authentication.
    
    Users can be either Clinic Admins or Patients.
    """
    __tablename__ = 'users'
    
    email = Column(String(320), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, index=True)
    
    # Relationships
    clinic_memberships = relationship('ClinicMembership', back_populates='user')
    patient = relationship('Patient', back_populates='user', uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role={self.role})>"
