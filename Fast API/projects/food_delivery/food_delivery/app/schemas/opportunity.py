from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OpportunityBase(BaseModel):
    title: str
    description: Optional[str] = None
    restaurant_name: str
    cuisine_type: Optional[str] = None
    price: float
    discount: Optional[float] = 0.0
    is_available: Optional[bool] = True
    image_url: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    restaurant_name: Optional[str] = None
    cuisine_type: Optional[str] = None
    price: Optional[float] = None
    discount: Optional[float] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None


class OpportunityResponse(OpportunityBase):
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
