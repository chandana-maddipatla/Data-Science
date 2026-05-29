# Test Plan — Task Manager Project

## 1. Project Name

Task Manager Application

---

## 2. Project Description

The Task Manager application is developed using React for the frontend and FastAPI for the backend. The application allows users to create, update, delete, search and filter tasks along with dashboard statistics.

The project also includes backend validations for Boundary Value Analysis and Domain Testing using FastAPI and Pydantic validations.

---

## 3. Objective

The objective of testing is to verify whether all functionalities of the application are working correctly and meet the project requirements.

The testing also verifies:
- Validation handling
- Boundary conditions
- Valid and invalid input domains
- Frontend and backend integration

---

## 4. Features to be Tested

- Login Functionality
- Create Task
- Update Task
- Delete Task
- Search Functionality
- Filter Functionality
- Dashboard Statistics
- Validation Messages
- API Responses
- Boundary Validations
- Domain Validations

---

## 5. Types of Testing Performed

- Functional Testing
- UI Testing
- Negative Testing
- Integration Testing
- Validation Testing
- Performance Testing
- Equivalence Partitioning (EP)
- Boundary Value Analysis (BVA)
- Domain Testing

---

## 6. Testing Environment

| Component | Details |
|---|---|
| Frontend | React |
| Backend | FastAPI |
| Frontend URL | http://localhost:5173 |
| Backend URL | http://127.0.0.1:8000 |
| API Docs | http://127.0.0.1:8000/docs |
| Browser | Google Chrome |

---

## 7. Tools Used

- FastAPI Swagger Docs
- React Frontend
- Excel Sheets for RTM and STLC
- Browser Developer Tools

---

## 8. Test Cases

Total Test Cases Prepared: 19

### Examples

- TC-001 — Valid Login
- TC-003 — Create Task
- TC-006 — Filter by Status
- TC-010 — Delete Confirmation Popup
- TC-012 — Stats Summary API
- TC-015 — Performance Testing
- TC-016 — Empty Title Boundary Validation
- TC-017 — Minimum Boundary Validation
- TC-018 — Maximum Boundary Validation
- TC-019 — Invalid Domain Validation

---

## 9. Equivalence Partitioning (EP)

Equivalence Partitioning was used by dividing inputs into:
- Valid partitions
- Invalid partitions

### Example

| Input | Partition Type | Result |
|---|---|---|
| Valid task title | Valid Partition | Task created successfully |
| Empty title | Invalid Partition | Validation error |

### Related Test Cases

- TC-003
- TC-004
- TC-016

---

## 10. Boundary Value Analysis (BVA)

Boundary Value Analysis was implemented using backend validations in FastAPI.

### Validation Added

python
title: str = Field(..., min_length=1, max_length=50)