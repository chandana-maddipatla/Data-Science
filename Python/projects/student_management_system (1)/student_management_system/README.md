# 🎓 AI Student Management System

A complete, production-style Python project that integrates **all core Python concepts** into a single, real-world application.

---

## 📁 Project Structure

```
student_management_system/
│
├── main.py           ← Entry point & menu-driven CLI
├── student.py        ← OOP: Student class + StudentRegistry
├── file_handler.py   ← File handling: read / write / export
├── auth.py           ← Authentication with dotenv
├── utils.py          ← Validation, lambdas, formatting helpers
├── decorators.py     ← @logger, @require_auth, @timer
├── generators.py     ← Generator functions for reports
├── .env              ← Admin credentials (never commit this!)
├── requirements.txt  ← Dependencies
├── students.txt      ← Persistent student data
└── README.md         ← This file
```

---

## 🧠 Python Concepts Covered

| Concept              | Where Used                          |
|----------------------|-------------------------------------|
| OOP (classes)        | `student.py` — Student, StudentRegistry |
| Functions            | All modules                         |
| File Handling        | `file_handler.py`                   |
| Exception Handling   | Throughout all modules              |
| Decorators           | `decorators.py` — @logger, @require_auth, @timer |
| Generators           | `generators.py` — yield, generator expressions |
| Lambda Functions     | `utils.py` — sort helpers           |
| Modules              | Separate `.py` files imported in `main.py` |
| dotenv               | `auth.py` — credentials from `.env` |
| Data Structures      | `student.py` — list + dict registry |
| Statements/Control   | `main.py` — menu if/elif/else       |
| Comparison Operators | `utils.py` — grade_to_letter()      |
| Properties           | `student.py` — @property setters with validation |
| Static/Class Methods | `student.py` — @staticmethod, @classmethod |

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the application
```bash
python main.py
```

### 3. Default Login
```
Username : admin
Password : admin123
```
> Change these in `.env` before sharing your project.

---

## ✨ Features

- **Add / Update / Delete** student records
- **Search** by ID, name, or course
- **Sort** by name, grade, age, or ID (using lambdas)
- **Reports**: statistics, top students, pass/fail, course-wise, paginated
- **Export** full report to `report.txt`
- **Persistent storage** — data saved to `students.txt` automatically
- **Activity log** — every operation logged to `activity.log`
- **Authentication** — login required for write operations
- **Decorators** in action — logging, auth guard, timing

---

## 📚 Learning Highlights

### Generator (memory-efficient iteration)
```python
def student_record_generator(registry):
    for student in registry.all():
        yield format_student_row(student)
```

### Lambda sorting
```python
students.sort(key=lambda s: s.grade, reverse=True)
```

### Decorator
```python
@logger
@require_auth
def add_student():
    ...
```

### dotenv usage
```python
from dotenv import load_dotenv
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
```

---

## 🗂 Sample Data
Eight sample students are pre-loaded in `students.txt` covering courses like Data Science, Machine Learning, Deep Learning, Computer Vision, and NLP.

---

## 💡 Extend This Project
- Add a **GUI** with Tkinter or a **web interface** with Flask
- Switch storage to **SQLite** or **PostgreSQL**
- Add **email notifications** for failing students
- Integrate a **REST API** with FastAPI
- Deploy to **cloud** with Docker

---

*Built as a portfolio project demonstrating integrated Python fundamentals.*
