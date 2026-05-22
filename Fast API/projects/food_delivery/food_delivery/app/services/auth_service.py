from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password
from app.core.config import settings
from jose import jwt
from datetime import datetime, timedelta


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def login(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        token = self._create_token({"sub": str(user.id), "email": user.email})
        return {"access_token": token, "token_type": "bearer"}

    def _create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
