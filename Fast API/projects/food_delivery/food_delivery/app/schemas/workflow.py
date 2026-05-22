from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import enum


class WorkflowStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class WorkflowBase(BaseModel):
    order_id: str
    user_id: int
    opportunity_id: int
    delivery_address: str
    notes: Optional[str] = None


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowUpdate(BaseModel):
    status: Optional[WorkflowStatus] = None
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class WorkflowResponse(WorkflowBase):
    id: int
    status: WorkflowStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
