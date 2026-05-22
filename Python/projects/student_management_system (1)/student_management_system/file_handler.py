"""
file_handler.py — Persistent storage for the Student Management System.

Covers:
    - File handling  (open / read / write / append in various modes)
    - Exception handling (FileNotFoundError, PermissionError, ValueError, etc.)
"""

import os
from student import Student, StudentRegistry
from decorators import logger
from utils import current_timestamp


DATA_FILE = os.getenv("DATA_FILE", "students.txt")


# ──────────────────────────────────────────────
# Low-level read / write
# ──────────────────────────────────────────────

@logger
def save_students(registry: StudentRegistry, filepath: str = DATA_FILE) -> bool:
    """
    Overwrite *filepath* with the current registry contents.
    Returns True on success, False on failure.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(f"# AI Student Management System — saved at {current_timestamp()}\n")
            for student in registry.all():
                fh.write(student.to_file_line() + "\n")
        print(f"✅  Data saved to '{filepath}' ({registry.count()} records).")
        return True
    except PermissionError:
        print(f"❌  Permission denied: cannot write to '{filepath}'.")
    except OSError as exc:
        print(f"❌  OS error while saving: {exc}")
    return False


@logger
def load_students(registry: StudentRegistry, filepath: str = DATA_FILE) -> bool:
    """
    Read student records from *filepath* into *registry*.
    Skips blank lines and comment lines (starting with #).
    Returns True on success, False if file not found.
    """
    try:
        students: list[Student] = []
        with open(filepath, "r", encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    students.append(Student.from_file_line(line))
                except ValueError as exc:
                    print(f"⚠️   Skipping malformed record on line {line_no}: {exc}")
        registry.load(students)
        print(f"✅  Loaded {registry.count()} records from '{filepath}'.")
        return True
    except FileNotFoundError:
        print(f"ℹ️   No existing data file found at '{filepath}'. Starting fresh.")
        return False
    except PermissionError:
        print(f"❌  Permission denied: cannot read '{filepath}'.")
    except OSError as exc:
        print(f"❌  OS error while loading: {exc}")
    return False


# ──────────────────────────────────────────────
# Export helpers
# ──────────────────────────────────────────────

@logger
def export_report(registry: StudentRegistry, filepath: str = "report.txt") -> bool:
    """Write a formatted text report of all students to *filepath*."""
    try:
        stats = registry.statistics()
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write("=" * 65 + "\n")
            fh.write("       AI STUDENT MANAGEMENT SYSTEM — FULL REPORT\n")
            fh.write(f"       Generated: {current_timestamp()}\n")
            fh.write("=" * 65 + "\n\n")

            if not stats:
                fh.write("  No student records found.\n")
            else:
                fh.write(f"  Total Students : {stats['total']}\n")
                fh.write(f"  Average Grade  : {stats['average']}\n")
                fh.write(f"  Highest Grade  : {stats['highest']}\n")
                fh.write(f"  Lowest Grade   : {stats['lowest']}\n")
                fh.write(f"  Passing        : {stats['passing']}\n")
                fh.write(f"  Failing        : {stats['failing']}\n\n")

                fh.write(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Course':<15} {'Grade':<7} {'Letter':<7} Status\n")
                fh.write("-" * 65 + "\n")
                for student in registry.all():
                    from utils import grade_to_letter, grade_to_status
                    letter = grade_to_letter(student.grade)
                    status = grade_to_status(student.grade)
                    fh.write(
                        f"{student.student_id:<10} {student.name:<20} {student.age:<5} "
                        f"{student.course:<15} {student.grade:<7.1f} {letter:<7} {status}\n"
                    )
        print(f"✅  Report exported to '{filepath}'.")
        return True
    except OSError as exc:
        print(f"❌  Could not write report: {exc}")
    return False


def read_log(log_file: str = "activity.log", tail: int = 20) -> None:
    """Print the last *tail* lines of the activity log."""
    try:
        with open(log_file, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
        recent = lines[-tail:] if len(lines) > tail else lines
        print(f"\n📋  Activity Log (last {len(recent)} entries):")
        print("-" * 50)
        for line in recent:
            print(line, end="")
        print()
    except FileNotFoundError:
        print("ℹ️   No activity log found yet.")
    except OSError as exc:
        print(f"❌  Could not read log: {exc}")
