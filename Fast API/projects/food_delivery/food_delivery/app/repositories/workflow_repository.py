from sqlalchemy.orm import Session
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate
from datetime import datetime


class WorkflowRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: WorkflowCreate):
        wf = Workflow(
            order_id=payload.order_id,
            user_id=payload.user_id,
            opportunity_id=payload.opportunity_id,
            delivery_address=payload.delivery_address,
            notes=payload.notes,
        )
        self.db.add(wf)
        self.db.commit()
        self.db.refresh(wf)
        return wf

    def get_by_id(self, workflow_id: int):
        return self.db.query(Workflow).filter(Workflow.id == workflow_id).first()

    def get_by_order_id(self, order_id: str):
        return self.db.query(Workflow).filter(Workflow.order_id == order_id).first()

    def list_workflows(self, status=None, user_id=None, skip=0, limit=10):
        query = self.db.query(Workflow)
        if status:
            query = query.filter(Workflow.status == status)
        if user_id:
            query = query.filter(Workflow.user_id == user_id)
        return query.offset(skip).limit(limit).all()

    def update(self, workflow_id: int, payload: WorkflowUpdate):
        wf = self.get_by_id(workflow_id)
        if not wf:
            return None
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(wf, key, value)
        wf.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(wf)
        return wf

    def delete(self, workflow_id: int):
        wf = self.get_by_id(workflow_id)
        if not wf:
            return False
        self.db.delete(wf)
        self.db.commit()
        return True
