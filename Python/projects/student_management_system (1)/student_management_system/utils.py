"""
utils.py — Helper / utility functions for the Student Management System.

Covers:
    - Input validation
    - Formatting helpers
    - Lambda-based sorting
    - Comparison-operator-based checks
"""

import re
from datetime import datetime


# ──────────────────────────────────────────────
# Validation helpers
# ──────────────────────────────────────────────

def validate_name(name: str) -> bool:
    """Return True if name contains only letters and spaces (min 2 chars)."""
    return bool(re.match(r"^[A-Za-z ]{2,}$", name.strip()))


def validate_student_id(sid: str) -> bool:
    """Student IDs must follow the pattern STU + 3-6 digits, e.g. STU001."""
    return bool(re.match(r"^STU\d{3,6}$", sid.strip().upper()))


def validate_age(age_str: str) -> bool:
    """Age must be an integer between 5 and 100."""
    try:
        age = int(age_str)
        return 5 <= age <= 100
    except ValueError:
        return False


def validate_grade(grade_str: str) -> bool:
    """Grade must be a float between 0.0 and 100.0."""
    try:
        grade = float(grade_str)
        return 0.0 <= grade <= 100.0
    except ValueError:
        return False


def validate_email(email: str) -> bool:
    """Basic e-mail format check."""
    return bool(re.match(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$", email.strip()))


# ──────────────────────────────────────────────
# Grade → letter conversion  (comparison operators)
# ──────────────────────────────────────────────

def grade_to_letter(grade: float) -> str:
    """Convert a numeric grade to a letter grade using comparison operators."""
    if grade >= 90:
        return "A+"
    elif grade >= 80:
        return "A"
    elif grade >= 70:
        return "B"
    elif grade >= 60:
        return "C"
    elif grade >= 50:
        return "D"
    else:
        return "F"


def grade_to_status(grade: float) -> str:
    return "PASS" if grade >= 50 else "FAIL"


# ──────────────────────────────────────────────
# Lambda-based sorting helpers
# ──────────────────────────────────────────────

sort_by_name        = lambda students: sorted(students, key=lambda s: s.name.lower())
sort_by_grade_desc  = lambda students: sorted(students, key=lambda s: s.grade, reverse=True)
sort_by_age         = lambda students: sorted(students, key=lambda s: s.age)
sort_by_id          = lambda students: sorted(students, key=lambda s: s.student_id)


# ──────────────────────────────────────────────
# Display / formatting helpers
# ──────────────────────────────────────────────

DIVIDER = "=" * 65


def print_header(title: str) -> None:
    print(f"\n{DIVIDER}")
    print(f"  {title.upper()}")
    print(DIVIDER)


def print_table_header() -> None:
    print(f"\n{'ID':<10} {'Name':<20} {'Age':<5} {'Course':<15} {'Grade':<7} {'Letter':<7} {'Status'}")
    print("-" * 65)


def format_student_row(student) -> str:
    letter = grade_to_letter(student.grade)
    status = grade_to_status(student.grade)
    return (
        f"{student.student_id:<10} {student.name:<20} {student.age:<5} "
        f"{student.course:<15} {student.grade:<7.1f} {letter:<7} {status}"
    )


def current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_input(prompt: str, allow_empty: bool = False) -> str:
    """A wrapper around input() that strips whitespace and handles EOF."""
    try:
        value = input(prompt).strip()
        if not allow_empty and value == "":
            raise ValueError("Input cannot be empty.")
        return value
    except EOFError:
        return ""
