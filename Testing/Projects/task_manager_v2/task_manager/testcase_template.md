# Test Case Template

| Field | Description |
|---|---|
| Test Case ID | Unique identifier for the test case |
| Test Case Name | Name of the test case |
| Test Type | Functional/UI/Negative/etc |
| Pre-Condition | Conditions before execution |
| Test Steps | Steps to execute the test |
| Test Data | Input values |
| Expected Result | Expected output |
| Actual Result | Actual output after execution |
| Status | Pass/Fail |

---

# Sample Test Case

| Field | Example |
|---|---|
| Test Case ID | TC-001 |
| Test Case Name | Valid Login |
| Test Type | Functional Testing |
| Pre-Condition | Backend running on port 8000 |
| Test Steps | Open Swagger Docs → Login → Execute |
| Test Data | admin / password |
| Expected Result | 200 OK with access token |
| Actual Result | Login successful |
| Status | Pass |

---

# Example Test Case — TC-003

## Test Case ID
TC-003

## Test Case Name
Create Task

## Test Type
Functional Testing

## Pre-Condition
Frontend and backend are running.

## Test Steps
1. Open http://localhost:5173
2. Click + New Task
3. Enter task details
4. Click Create

## Test Data
Title: My Test Task
Priority: High
Status: Open

## Expected Result
Task appears in the table.

## Actual Result
Task created successfully.

## Status
Pass