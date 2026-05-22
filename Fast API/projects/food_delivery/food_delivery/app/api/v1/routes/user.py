from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.dependencies.auth_dependency import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    existing = service.get_by_email(user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return service.create(user)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    token = service.login(credentials.email, credentials.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return token


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = UserService(db)
    return service.list_users(name=name, is_active=is_active, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = UserService(db)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = UserService(db)
    user = service.update(user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    service = UserService(db)
    if not service.delete(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
