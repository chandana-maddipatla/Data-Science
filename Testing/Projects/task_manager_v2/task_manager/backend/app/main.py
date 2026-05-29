from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import uuid
import re

app = FastAPI(title="Task Manager API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

DEMO_TOKEN = "demo-jwt-token-taskmanager"

# ── In-memory DB ─────────────────────────────────────────────
tasks_db: dict = {}

SEED = [
    {
        "title": "Setup authentication module",
        "description": "Implement JWT login flow",
        "status": "Closed",
        "priority": "Critical",
        "module": "Auth",
        "assigned_to": "Alice"
    },
    {
        "title": "Create task CRUD endpoints",
        "description": "POST/GET/PUT/DELETE for tasks",
        "status": "Closed",
        "priority": "High",
        "module": "Task Management",
        "assigned_to": "Bob"
    },
]

for item in SEED:
    tid = str(uuid.uuid4())

    tasks_db[tid] = {
        **item,
        "id": tid,
        "created_at": datetime.now().isoformat()
    }

# ── Models ───────────────────────────────────────────────────

class TaskCreate(BaseModel):

    # Boundary Value Analysis (BVA)

    title: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Task title must be between 1 and 50 characters"
    )

    # Domain Testing

    status: str = Field(
        default="Open",
        pattern="^(Open|In Progress|Closed)$"
    )

    priority: str = Field(
        default="Medium",
        pattern="^(Low|Medium|High|Critical)$"
    )

    assigned_to: Optional[str] = Field(
        default="",
        max_length=30
    )

    description: Optional[str] = ""
    module: str = "General"


class TaskUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    status: Optional[str] = Field(
        default=None,
        pattern="^(Open|In Progress|Closed)$"
    )

    priority: Optional[str] = Field(
        default=None,
        pattern="^(Low|Medium|High|Critical)$"
    )

    assigned_to: Optional[str] = Field(
        default=None,
        max_length=30
    )

    description: Optional[str] = None
    module: Optional[str] = None


class LoginRequest(BaseModel):

    # Boundary Value Analysis

    username: str = Field(
        ...,
        min_length=3,
        max_length=20
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=14
    )

    # Domain Testing + Validation Testing

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        # Uppercase validation
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        # Lowercase validation
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        # Number validation
        if not re.search(r"[0-9]", value):
            raise ValueError(
                "Password must contain at least one number"
            )

        # Special character validation
        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value
        ):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return value


# ── Auth ─────────────────────────────────────────────────────

def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security)
):

    if creds and creds.credentials == DEMO_TOKEN:
        return "admin"

    return "guest"


# ── Routes ───────────────────────────────────────────────────

@app.post("/auth/login")
def login(body: LoginRequest):

    if (
        body.username == "admin"
        and body.password == "Admin@123"
    ):

        return {
            "access_token": DEMO_TOKEN,
            "token_type": "bearer",
            "username": "admin"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "version": "2.0.0"
    }


@app.get("/tasks/stats/summary")
def get_stats():

    tasks = list(tasks_db.values())

    total = len(tasks)

    by_status = {}
    by_priority = {}

    for t in tasks:

        by_status[t["status"]] = (
            by_status.get(t["status"], 0) + 1
        )

        by_priority[t["priority"]] = (
            by_priority.get(t["priority"], 0) + 1
        )

    return {
        "total": total,
        "by_status": by_status,
        "by_priority": by_priority
    }


@app.get("/tasks")
def list_tasks(

    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),

):

    tasks = list(tasks_db.values())

    if status:
        tasks = [
            t for t in tasks
            if t["status"] == status
        ]

    if priority:
        tasks = [
            t for t in tasks
            if t["priority"] == priority
        ]

    if search:

        s = search.lower()

        tasks = [
            t for t in tasks
            if s in t["title"].lower()
            or s in t.get("description", "").lower()
        ]

    return tasks


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):

    tid = str(uuid.uuid4())

    task = {
        **body.dict(),
        "id": tid,
        "created_at": datetime.now().isoformat()
    }

    tasks_db[tid] = task

    return task


@app.get("/tasks/{task_id}")
def get_task(task_id: str):

    if task_id not in tasks_db:

        raise HTTPException(
            status_code=404,
            detail=f"Task '{task_id}' not found"
        )

    return tasks_db[task_id]


@app.put("/tasks/{task_id}")
def update_task(task_id: str, body: TaskUpdate):

    if task_id not in tasks_db:

        raise HTTPException(
            status_code=404,
            detail=f"Task '{task_id}' not found"
        )

    for k, v in body.dict(exclude_none=True).items():
        tasks_db[task_id][k] = v

    return tasks_db[task_id]


@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):

    if task_id not in tasks_db:

        raise HTTPException(
            status_code=404,
            detail=f"Task '{task_id}' not found"
        )

    del tasks_db[task_id]

    return {
        "deleted": task_id
    }