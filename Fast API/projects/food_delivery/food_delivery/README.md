# Food Delivery Project

A FastAPI-based REST API for a food delivery platform.

## Features
- User management (registration, login, profile)
- Opportunity/restaurant listing management
- Workflow management for order processing

## Project Structure
```
food_delivery_project/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── opportunity.py
│   │       │   ├── user.py
│   │       │   └── workflow.py
│   │       └── router.py
│   ├── models/
│   │   ├── opportunity.py
│   │   ├── user.py
│   │   └── workflow.py
│   ├── schemas/
│   │   ├── opportunity.py
│   │   ├── user.py
│   │   └── workflow.py
│   ├── __init__.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Setup & Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **API Documentation**
   Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## API Endpoints

### Users
- `POST /api/v1/users/register` — Register new user
- `POST /api/v1/users/login` — Login
- `GET /api/v1/users/{user_id}` — Get user by ID
- `PUT /api/v1/users/{user_id}` — Update user
- `DELETE /api/v1/users/{user_id}` — Delete user

### Opportunities
- `POST /api/v1/opportunities/` — Create opportunity
- `GET /api/v1/opportunities/` — List all opportunities
- `GET /api/v1/opportunities/{opportunity_id}` — Get opportunity
- `PUT /api/v1/opportunities/{opportunity_id}` — Update opportunity
- `DELETE /api/v1/opportunities/{opportunity_id}` — Delete opportunity

### Workflows
- `POST /api/v1/workflows/` — Create workflow
- `GET /api/v1/workflows/` — List all workflows
- `GET /api/v1/workflows/{workflow_id}` — Get workflow
- `PUT /api/v1/workflows/{workflow_id}` — Update workflow
- `DELETE /api/v1/workflows/{workflow_id}` — Delete workflow
