from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    restaurant_name = Column(String(150), nullable=False)
    cuisine_type = Column(String(100), nullable=True)
    price = Column(Float, nullable=False, default=0.0)
    discount = Column(Float, nullable=True, default=0.0)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(500), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="opportunities")
    workflows = relationship("Workflow", back_populates="opportunity")
