import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    with open(path, "w") as f:
        f.write(content)
    print(f"✅ written: {path}")

# ── schemas/auth.py
write("app/schemas/auth.py", '''from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
''')

# ── routes/auth.py
write("app/api/v1/routes/auth.py", '''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()


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


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout():
    return {"message": "Logged out successfully"}
''')

# ── routes/user.py
write("app/api/v1/routes/user.py", '''from fastapi import APIRouter, Depends, HTTPException, status
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
''')

# ── routes/opportunity.py
write("app/api/v1/routes/opportunity.py", '''from fastapi import APIRouter, Depends, HTTPException, status
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
''')

# ── routes/workflow.py
write("app/api/v1/routes/workflow.py", '''from fastapi import APIRouter, Depends, HTTPException, status
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
''')

# ── dependencies/auth_dependency.py
write("app/dependencies/auth_dependency.py", '''from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except JWTError:
        raise credentials_exception
''')

# ── services/auth_service.py
write("app/services/auth_service.py", '''from sqlalchemy.orm import Session
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
''')

# ── services/user_service.py
write("app/services/user_service.py", '''from sqlalchemy.orm import Session
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
''')

# ── services/opportunity_service.py
write("app/services/opportunity_service.py", '''from sqlalchemy.orm import Session
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
''')

# ── services/workflow_service.py
write("app/services/workflow_service.py", '''from sqlalchemy.orm import Session
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
''')

# ── repositories/user_repository.py
write("app/repositories/user_repository.py", '''from sqlalchemy.orm import Session
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
''')

# ── repositories/opportunity_repository.py
write("app/repositories/opportunity_repository.py", '''from sqlalchemy.orm import Session
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
''')

# ── repositories/workflow_repository.py
write("app/repositories/workflow_repository.py", '''from sqlalchemy.orm import Session
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
''')

# ── middleware/logging.py
write("app/middleware/logging.py", '''import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("food_delivery")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = round((time.time() - start) * 1000, 2)
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration}ms)")
        return response
''')

# ── middleware/auth.py
write("app/middleware/auth.py", '''from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

EXCLUDED_PATHS = [
    "/",
    "/docs",
    "/openapi.json",
    "/api/v1/users/register",
    "/api/v1/auth/login",
    "/api/v1/users/login"
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "Missing or invalid authorization header"}
            )
        return await call_next(request)
''')

# ── utils/logger.py
write("app/utils/logger.py", '''import logging
import sys


def setup_logger(name: str = "food_delivery") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = setup_logger()
''')

# ── utils/helper.py
write("app/utils/helper.py", '''from datetime import datetime


def current_timestamp() -> datetime:
    return datetime.utcnow()


def paginate(query_list: list, skip: int = 0, limit: int = 10) -> list:
    return query_list[skip: skip + limit]


def normalize_string(value: str) -> str:
    return value.strip().lower() if value else value
''')

# ── utils/common.py
write("app/utils/common.py", '''from typing import Any


def success_response(data: Any, message: str = "Success") -> dict:
    return {"status": "success", "message": message, "data": data}


def error_response(message: str, code: int = 400) -> dict:
    return {"status": "error", "message": message, "code": code}
''')

# ── tests/test_user.py
write("app/tests/test_user.py", '''from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    response = client.post("/api/v1/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
        "phone": "9999999999",
        "address": "Test Address"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"


def test_register_duplicate_email():
    client.post("/api/v1/users/register", json={
        "name": "Test User",
        "email": "dup@example.com",
        "password": "testpassword"
    })
    response = client.post("/api/v1/users/register", json={
        "name": "Test User 2",
        "email": "dup@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 400


def test_get_user_not_found():
    response = client.get("/api/v1/users/9999")
    assert response.status_code in [401, 404]
''')

# ── tests/test_auth.py
write("app/tests/test_auth.py", '''from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_invalid_credentials():
    response = client.post("/api/v1/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_success():
    client.post("/api/v1/users/register", json={
        "name": "Auth User",
        "email": "authuser@example.com",
        "password": "securepass"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "authuser@example.com",
        "password": "securepass"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
''')

# ── Dockerfile
write("Dockerfile", '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# ── docker-compose.yml
write("docker-compose.yml", '''version: "3.9"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: yourpassword
      MYSQL_DATABASE: food_delivery
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
''')

# ── router.py — updated to include auth
write("app/api/v1/router.py", '''from fastapi import APIRouter
from app.api.v1.routes import user, opportunity, workflow, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(opportunity.router, prefix="/opportunities", tags=["Opportunities"])
api_router.include_router(workflow.router, prefix="/workflows", tags=["Workflows"])
''')

print("\n✅ All files written successfully!")
print("\nNow run:")
print("  pip install python-jose passlib bcrypt pymysql sqlalchemy pydantic-settings python-dotenv")
print("  uvicorn app.main:app --reload")