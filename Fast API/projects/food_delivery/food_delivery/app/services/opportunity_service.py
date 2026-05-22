from sqlalchemy.orm import Session
from app.repositories.opportunity_repository import OpportunityRepository
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate


class OpportunityService:
    def __init__(self, db: Session):
        self.repo = OpportunityRepository(db)

    def create(self, payload: OpportunityCreate, created_by: int = None):
        return self.repo.create(payload, created_by)

    def get_by_id(self, opp_id: int):
        return self.repo.get_by_id(opp_id)

    def list_opportunities(self, restaurant_name=None, cuisine_type=None, is_available=None, skip=0, limit=10):
        return self.repo.list_opportunities(
            restaurant_name=restaurant_name,
            cuisine_type=cuisine_type,
            is_available=is_available,
            skip=skip,
            limit=limit
        )

    def update(self, opp_id: int, payload: OpportunityUpdate):
        return self.repo.update(opp_id, payload)

    def delete(self, opp_id: int):
        return self.repo.delete(opp_id)
