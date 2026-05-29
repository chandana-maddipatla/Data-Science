# Types of Testing

## Functional Testing
Purpose:
To verify that application features work correctly.

Examples:
- Create Task
- Edit Task
- Delete Task
- Login

Related Test Cases:
- TC-001
- TC-003
- TC-005
- TC-008

---

## Negative Testing
Purpose:
To verify how the system handles invalid inputs.

Examples:
- Invalid login
- Empty title
- Invalid task ID

Related Test Cases:
- TC-002
- TC-004
- TC-009

---

## UI Testing
Purpose:
To verify frontend behavior and user interactions.

Examples:
- Delete confirmation popup
- Search box
- Filter dropdowns

Related Test Cases:
- TC-006
- TC-007
- TC-010
- TC-011

---

## Integration Testing
Purpose:
To verify communication between frontend and backend.

Examples:
- Stats dashboard updates
- Task creation updates table

Related Test Cases:
- TC-012
- TC-014

---

## Validation Testing
Purpose:
To verify mandatory field validation and error messages.

Examples:
- Empty title validation
- Invalid credentials validation

Related Test Cases:
- TC-002
- TC-004

---

## Performance Testing
Purpose:
To verify API response speed and application performance.

Examples:
- Stats API response under 1 second

Related Test Cases:
- TC-015
---

## Equivalence Partitioning (EP)

Equivalence Partitioning is a testing technique where input data is divided into:
- Valid partitions
- Invalid partitions

One representative value is tested from each partition.

### Example in Task Manager Project

| Input | Partition Type | Result |
|---|---|---|
| Valid task title | Valid Partition | Task created successfully |
| Empty title | Invalid Partition | Validation error displayed |

Related Test Cases:
- TC-003
- TC-004

---

## Boundary Value Analysis (BVA)

Boundary Value Analysis is used to test values near minimum and maximum limits.

In the Task Manager project, boundary validations were added for the task title field using Pydantic validation in FastAPI.

### Validation Added

- Minimum Length = 1
- Maximum Length = 50

### Boundary Test Cases

| Test Value | Type | Expected Result |
|---|---|---|
| Empty title | Invalid Boundary | Validation error |
| 1 character title | Minimum Valid Boundary | Accepted |
| 50 character title | Maximum Valid Boundary | Accepted |
| 51 character title | Invalid Boundary | Validation error |

The validations were tested using FastAPI Swagger Docs.

---

## Domain Testing

Domain Testing is used to verify whether only valid input values are accepted by the system.

In the project, domain validations were added for:
- Status field
- Priority field

### Valid Status Values
- Open
- In Progress
- Closed

### Valid Priority Values
- Low
- Medium
- High
- Critical

### Example

| Input | Result |
|---|---|
| Open | Valid |
| Done | Invalid |
| High | Valid |
| Urgent | Invalid |

These validations were implemented using pattern validation in FastAPI.