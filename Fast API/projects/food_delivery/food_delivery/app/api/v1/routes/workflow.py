from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse, WorkflowStatus
from app.services.workflow_service import WorkflowService
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(
    payload: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = WorkflowService(db)
    if service.get_by_order_id(payload.order_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order ID already exists")
    return service.create(payload)


@router.get("/", response_model=List[WorkflowResponse], status_code=status.HTTP_200_OK)
def list_workflows(
    status: Optional[WorkflowStatus] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = WorkflowService(db)
    return service.list_workflows(status=status, user_id=user_id, skip=skip, limit=limit)


@router.get("/{workflow_id}", response_model=WorkflowResponse, status_code=status.HTTP_200_OK)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = WorkflowService(db)
    wf = service.get_by_id(workflow_id)
    if not wf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return wf


@router.put("/{workflow_id}", response_model=WorkflowResponse, status_code=status.HTTP_200_OK)
def update_workflow(
    workflow_id: int,
    payload: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = WorkflowService(db)
    wf = service.update(workflow_id, payload)
    if not wf:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return wf


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = WorkflowService(db)
    if not service.delete(workflow_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
