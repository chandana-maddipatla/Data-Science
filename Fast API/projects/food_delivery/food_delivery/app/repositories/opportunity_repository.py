from sqlalchemy.orm import Session
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate
from datetime import datetime


class OpportunityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: OpportunityCreate, created_by: int = None):
        opp = Opportunity(
            title=payload.title,
            description=payload.description,
            restaurant_name=payload.restaurant_name,
            cuisine_type=payload.cuisine_type,
            price=payload.price,
            discount=payload.discount,
            is_available=payload.is_available,
            image_url=payload.image_url,
            created_by=created_by,
        )
        self.db.add(opp)
        self.db.commit()
        self.db.refresh(opp)
        return opp

    def get_by_id(self, opp_id: int):
        return self.db.query(Opportunity).filter(Opportunity.id == opp_id).first()

    def list_opportunities(self, restaurant_name=None, cuisine_type=None, is_available=None, skip=0, limit=10):
        query = self.db.query(Opportunity)
        if restaurant_name:
            query = query.filter(Opportunity.restaurant_name.ilike(f"%{restaurant_name}%"))
        if cuisine_type:
            query = query.filter(Opportunity.cuisine_type.ilike(f"%{cuisine_type}%"))
        if is_available is not None:
            query = query.filter(Opportunity.is_available == is_available)
        return query.offset(skip).limit(limit).all()

    def update(self, opp_id: int, payload: OpportunityUpdate):
        opp = self.get_by_id(opp_id)
        if not opp:
            return None
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(opp, key, value)
        opp.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(opp)
        return opp

    def delete(self, opp_id: int):
        opp = self.get_by_id(opp_id)
        if not opp:
            return False
        self.db.delete(opp)
        self.db.commit()
        return True
