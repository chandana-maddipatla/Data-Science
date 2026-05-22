from sqlalchemy.orm import Session
from app.repositories.workflow_repository import WorkflowRepository
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate


class WorkflowService:
    def __init__(self, db: Session):
        self.repo = WorkflowRepository(db)

    def create(self, payload: WorkflowCreate):
        return self.repo.create(payload)

    def get_by_id(self, workflow_id: int):
        return self.repo.get_by_id(workflow_id)

    def get_by_order_id(self, order_id: str):
        return self.repo.get_by_order_id(order_id)

    def list_workflows(self, status=None, user_id=None, skip=0, limit=10):
        return self.repo.list_workflows(status=status, user_id=user_id, skip=skip, limit=limit)

    def update(self, workflow_id: int, payload: WorkflowUpdate):
        return self.repo.update(workflow_id, payload)

    def delete(self, workflow_id: int):
        return self.repo.delete(workflow_id)
