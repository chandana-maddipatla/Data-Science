from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunityResponse
from app.services.opportunity_service import OpportunityService
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


@router.post("/", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(
    payload: OpportunityCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = OpportunityService(db)
    return service.create(payload, created_by=current_user)


@router.get("/", response_model=List[OpportunityResponse], status_code=status.HTTP_200_OK)
def list_opportunities(
    restaurant_name: Optional[str] = None,
    cuisine_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    service = OpportunityService(db)
    return service.list_opportunities(
        restaurant_name=restaurant_name,
        cuisine_type=cuisine_type,
        is_available=is_available,
        skip=skip,
        limit=limit
    )


@router.get("/{opportunity_id}", response_model=OpportunityResponse, status_code=status.HTTP_200_OK)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    service = OpportunityService(db)
    opp = service.get_by_id(opportunity_id)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
    return opp


@router.put("/{opportunity_id}", response_model=OpportunityResponse, status_code=status.HTTP_200_OK)
def update_opportunity(
    opportunity_id: int,
    payload: OpportunityUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = OpportunityService(db)
    opp = service.update(opportunity_id, payload)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
    return opp


@router.delete("/{opportunity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_opportunity(
    opportunity_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = OpportunityService(db)
    if not service.delete(opportunity_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
