from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create(self, user: UserCreate):
        hashed = hash_password(user.password)
        return self.repo.create(user, hashed)

    def get_by_id(self, user_id: int):
        return self.repo.get_by_id(user_id)

    def get_by_email(self, email: str):
        return self.repo.get_by_email(email)

    def list_users(self, name=None, is_active=None, skip=0, limit=10):
        return self.repo.list_users(name=name, is_active=is_active, skip=skip, limit=limit)

    def update(self, user_id: int, payload: UserUpdate):
        return self.repo.update(user_id, payload)

    def delete(self, user_id: int):
        return self.repo.delete(user_id)
