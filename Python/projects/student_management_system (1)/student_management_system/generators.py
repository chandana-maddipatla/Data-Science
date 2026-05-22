"""
generators.py — Generator functions for the Student Management System.

Covers:
    - yield-based generators (memory-efficient iteration)
    - Generator expressions
    - Using generators for report streaming
"""

from student import Student, StudentRegistry
from utils import grade_to_letter, grade_to_status


# ──────────────────────────────────────────────
# 1.  Student record generator
# ──────────────────────────────────────────────

def student_record_generator(registry: StudentRegistry):
    """
    Yield one formatted student record string at a time.
    Memory-efficient: doesn't build the full report in RAM.
    """
    for student in registry.all():
        letter = grade_to_letter(student.grade)
        status = grade_to_status(student.grade)
        yield (
            f"{student.student_id:<10} {student.name:<20} {student.age:<5} "
            f"{student.course:<15} {student.grade:<7.1f} {letter:<7} {status}"
        )


# ──────────────────────────────────────────────
# 2.  Filtered generators
# ──────────────────────────────────────────────

def passing_students_generator(registry: StudentRegistry):
    """Yield only students who are passing (grade >= 50)."""
    for student in registry.all():
        if student.grade >= 50:
            yield student


def failing_students_generator(registry: StudentRegistry):
    """Yield only students who are failing (grade < 50)."""
    for student in registry.all():
        if student.grade < 50:
            yield student


def top_students_generator(registry: StudentRegistry, top_n: int = 5):
    """Yield the top *top_n* students sorted by grade descending."""
    sorted_students = sorted(registry.all(), key=lambda s: s.grade, reverse=True)
    for student in sorted_students[:top_n]:
        yield student


# ──────────────────────────────────────────────
# 3.  Grade summary generator  (generator expression example)
# ──────────────────────────────────────────────

def grade_summary_generator(registry: StudentRegistry):
    """
    Yield (student_id, name, letter_grade) tuples using a generator expression
    for every student in the registry.
    """
    return (
        (s.student_id, s.name, grade_to_letter(s.grade))
        for s in registry.all()
    )


# ──────────────────────────────────────────────
# 4.  Paginated report generator
# ──────────────────────────────────────────────

def paginated_report_generator(registry: StudentRegistry, page_size: int = 5):
    """
    Yield pages (lists of Student objects) of size *page_size*.
    Useful for displaying large datasets screen-by-screen.
    """
    all_students = registry.all()
    for i in range(0, len(all_students), page_size):
        yield all_students[i : i + page_size]


# ──────────────────────────────────────────────
# 5.  Course statistics generator
# ──────────────────────────────────────────────

def course_stats_generator(registry: StudentRegistry):
    """
    Yield (course_name, count, avg_grade) for every unique course.
    Demonstrates generator over a grouped data structure (dict).
    """
    course_map: dict[str, list[float]] = {}
    for student in registry.all():
        course_map.setdefault(student.course, []).append(student.grade)

    for course, grades in sorted(course_map.items()):
        avg = round(sum(grades) / len(grades), 2)
        yield course, len(grades), avg
