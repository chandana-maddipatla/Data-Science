from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from datetime import datetime


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate, hashed_password: str):
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
            phone=user.phone,
            address=user.address,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def list_users(self, name=None, is_active=None, skip=0, limit=10):
        query = self.db.query(User)
        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        return query.offset(skip).limit(limit).all()

    def update(self, user_id: int, payload: UserUpdate):
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
