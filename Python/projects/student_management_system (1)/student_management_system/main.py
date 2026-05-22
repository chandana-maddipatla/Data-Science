"""
main.py — Entry point for the AI Student Management System.

Covers:
    - Menu-driven CLI (if/elif/else statements)
    - Integrates ALL modules: student, file_handler, auth, utils,
      decorators, generators
    - Exception handling throughout
    - dotenv loaded via auth import
"""

import os
from dotenv import load_dotenv

# Load .env before anything that reads env vars
load_dotenv()

from student      import Student, StudentRegistry
from file_handler import save_students, load_students, export_report, read_log
from auth         import AuthManager
from decorators   import logger, require_auth, timer
from generators   import (
    student_record_generator,
    passing_students_generator,
    failing_students_generator,
    top_students_generator,
    grade_summary_generator,
    paginated_report_generator,
    course_stats_generator,
)
from utils import (
    print_header, print_table_header, format_student_row,
    safe_input, sort_by_name, sort_by_grade_desc,
    sort_by_age, sort_by_id, DIVIDER
)

APP_NAME = os.getenv("APP_NAME", "AI Student Management System")
VERSION  = os.getenv("VERSION", "1.0.0")

# Global registry — single source of truth for this session
registry = StudentRegistry()


# ══════════════════════════════════════════════
# Add / Edit / Delete
# ══════════════════════════════════════════════

@logger
@require_auth
def add_student() -> None:
    print_header("Add New Student")
    try:
        name   = safe_input("  Name        : ")
        age    = safe_input("  Age         : ")
        course = safe_input("  Course      : ")
        grade  = safe_input("  Grade(0-100): ")
        email  = safe_input("  Email       : ")

        student = Student(
            name=name, age=int(age),
            course=course, grade=float(grade), email=email
        )
        registry.add(student)
        print(f"\n  ✅  Student added successfully!\n{student}")
        save_students(registry)

    except ValueError as exc:
        print(f"\n  ❌  Validation error: {exc}")
    except Exception as exc:
        print(f"\n  ❌  Unexpected error: {exc}")


@logger
@require_auth
def update_student() -> None:
    print_header("Update Student")
    try:
        sid = safe_input("  Enter Student ID to update : ").upper()
        student = registry.get_by_id(sid)
        if not student:
            print(f"  ❌  Student '{sid}' not found.")
            return
        print(f"\n  Current record:\n{student}\n")
        print("  (Press Enter to keep current value)\n")

        fields = {}
        name = input(f"  New Name   [{student.name}] : ").strip()
        if name:
            fields["name"] = name

        age = input(f"  New Age    [{student.age}] : ").strip()
        if age:
            fields["age"] = int(age)

        course = input(f"  New Course [{student.course}] : ").strip()
        if course:
            fields["course"] = course

        grade = input(f"  New Grade  [{student.grade}] : ").strip()
        if grade:
            fields["grade"] = float(grade)

        email = input(f"  New Email  [{student.email}] : ").strip()
        if email:
            fields["email"] = email

        if fields:
            registry.update(sid, **fields)
            print(f"\n  ✅  Student updated.\n{registry.get_by_id(sid)}")
            save_students(registry)
        else:
            print("  ℹ️   No changes made.")

    except ValueError as exc:
        print(f"\n  ❌  Validation error: {exc}")


@logger
@require_auth
def delete_student() -> None:
    print_header("Delete Student")
    try:
        sid = safe_input("  Enter Student ID to delete : ").upper()
        student = registry.get_by_id(sid)
        if not student:
            print(f"  ❌  Student '{sid}' not found.")
            return
        print(f"\n  Record to delete:\n{student}")
        confirm = safe_input("\n  Confirm delete? (yes/no) : ").lower()
        if confirm == "yes":
            registry.delete(sid)
            print(f"  ✅  Student '{sid}' deleted.")
            save_students(registry)
        else:
            print("  ℹ️   Deletion cancelled.")
    except ValueError as exc:
        print(f"\n  ❌  {exc}")


# ══════════════════════════════════════════════
# Search / Display
# ══════════════════════════════════════════════

def search_student() -> None:
    print_header("Search Student")
    print("  1. Search by ID")
    print("  2. Search by Name")
    print("  3. Search by Course")

    try:
        choice = input("\n  Select (1-3) : ").strip()

        if choice == "1":
            sid = input("  Enter Student ID (e.g. STU001) : ").strip().upper()
            if not sid:
                print("  ❌  Please enter a Student ID.")
                return
            student = registry.get_by_id(sid)
            if student:
                print(f"\n{student}")
            else:
                print(f"  ❌  No student found with ID '{sid}'.")

        elif choice == "2":
            query = input("  Enter Name (partial match allowed) : ").strip()
            if not query:
                print("  ❌  Please enter a name to search.")
                return
            results = registry.search_by_name(query)
            if results:
                print(f"\n  Found {len(results)} result(s):")
                print_table_header()
                for s in results:
                    print(format_student_row(s))
            else:
                print(f"  ❌  No students found matching '{query}'.")

        elif choice == "3":
            course = input("  Enter Course name (partial match allowed) : ").strip()
            if not course:
                print("  ❌  Please enter a course name to search.")
                return
            results = registry.search_by_course(course)
            if results:
                print(f"\n  Found {len(results)} result(s):")
                print_table_header()
                for s in results:
                    print(format_student_row(s))
            else:
                print(f"  ❌  No students found in course matching '{course}'.")
                print(f"  ℹ️   Available courses: {', '.join(sorted(set(s.course for s in registry.all())))}")

        else:
            print("  ❌  Invalid choice. Please enter 1, 2, or 3.")

    except Exception as exc:
        print(f"  ❌  Search error: {exc}")


def display_all_students() -> None:
    print_header("All Students")
    print("  Sort by: 1=Name  2=Grade↓  3=Age  4=ID")
    choice = safe_input("  Select sort (1-4, default=4) : ", allow_empty=True) or "4"

    students = registry.all()
    if not students:
        print("  ℹ️   No students in the system yet.")
        return

    sorters = {
        "1": sort_by_name,
        "2": sort_by_grade_desc,
        "3": sort_by_age,
        "4": sort_by_id,
    }
    sorter   = sorters.get(choice, sort_by_id)
    students = sorter(students)

    print_table_header()
    tmp = StudentRegistry()
    tmp.load(students)
    for row in student_record_generator(tmp):
        print(row)
    print(f"\n  Total: {registry.count()} student(s)")


# ══════════════════════════════════════════════
# Reports
# ══════════════════════════════════════════════

@timer
def show_statistics() -> None:
    print_header("Statistics")
    stats = registry.statistics()
    if not stats:
        print("  ℹ️   No data available.")
        return
    print(f"  Total Students  : {stats['total']}")
    print(f"  Average Grade   : {stats['average']}")
    print(f"  Highest Grade   : {stats['highest']}")
    print(f"  Lowest Grade    : {stats['lowest']}")
    print(f"  Passing (≥50)   : {stats['passing']}")
    print(f"  Failing (<50)   : {stats['failing']}")


def show_top_students() -> None:
    print_header("Top 5 Students")
    found = False
    print_table_header()
    for student in top_students_generator(registry, top_n=5):
        print(format_student_row(student))
        found = True
    if not found:
        print("  ℹ️   No students found.")


def show_pass_fail() -> None:
    print_header("Pass / Fail Report")
    print("\n  ── PASSING STUDENTS ──")
    passing = list(passing_students_generator(registry))
    if passing:
        print_table_header()
        for s in passing:
            print(format_student_row(s))
    else:
        print("  (none)")

    print("\n  ── FAILING STUDENTS ──")
    failing = list(failing_students_generator(registry))
    if failing:
        print_table_header()
        for s in failing:
            print(format_student_row(s))
    else:
        print("  (none)")


def show_course_stats() -> None:
    print_header("Course-wise Statistics")
    print(f"\n  {'Course':<20} {'Students':<10} {'Avg Grade'}")
    print("  " + "-" * 40)
    found = False
    for course, count, avg in course_stats_generator(registry):
        print(f"  {course:<20} {count:<10} {avg}")
        found = True
    if not found:
        print("  ℹ️   No data available.")


def show_grade_summary() -> None:
    print_header("Grade Summary (generator expression)")
    print(f"\n  {'ID':<10} {'Name':<20} {'Letter Grade'}")
    print("  " + "-" * 38)
    for sid, name, letter in grade_summary_generator(registry):
        print(f"  {sid:<10} {name:<20} {letter}")


def show_paginated() -> None:
    print_header("Browse Students (Paginated)")
    pages = list(paginated_report_generator(registry, page_size=5))
    if not pages:
        print("  ℹ️   No students found.")
        return
    for page_no, page in enumerate(pages, start=1):
        print(f"\n  ── Page {page_no} of {len(pages)} ──")
        print_table_header()
        for s in page:
            print(format_student_row(s))
        if page_no < len(pages):
            cont = input("\n  Press Enter for next page (or 'q' to quit) : ").strip().lower()
            if cont == "q":
                break


# ══════════════════════════════════════════════
# Menus
# ══════════════════════════════════════════════

def reports_menu() -> None:
    while True:
        print_header("Reports Menu")
        print("  1. Statistics Summary")
        print("  2. Top 5 Students")
        print("  3. Pass / Fail Report")
        print("  4. Course-wise Stats")
        print("  5. Grade Summary")
        print("  6. Browse Paginated")
        print("  7. Export Full Report to File")
        print("  0. Back")
        choice = safe_input("\n  Select : ", allow_empty=True) or "0"

        if choice == "1":
            show_statistics()
        elif choice == "2":
            show_top_students()
        elif choice == "3":
            show_pass_fail()
        elif choice == "4":
            show_course_stats()
        elif choice == "5":
            show_grade_summary()
        elif choice == "6":
            show_paginated()
        elif choice == "7":
            export_report(registry)
        elif choice == "0":
            break
        else:
            print("  ❌  Invalid option.")

        input("\n  Press Enter to continue...")


def main_menu() -> None:
    while True:
        print(f"\n{DIVIDER}")
        print(f"   🎓  {APP_NAME}  v{VERSION}")
        user_info = f"  Logged in as: {AuthManager.current_user()}" if AuthManager.is_logged_in() else "  Not logged in"
        print(f"   {user_info}")
        print(DIVIDER)
        print("  1. Add Student")
        print("  2. View All Students")
        print("  3. Search Student")
        print("  4. Update Student")
        print("  5. Delete Student")
        print("  6. Reports & Analytics")
        print("  7. View Activity Log")
        print("  8. Change Password")
        print("  9. Save Data")
        print("  L. Login / Logout")
        print("  0. Exit")
        print(DIVIDER)

        choice = safe_input("  Select option : ", allow_empty=True).upper() or "0"

        if choice == "1":
            add_student()
        elif choice == "2":
            display_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            reports_menu()
        elif choice == "7":
            read_log()
        elif choice == "8":
            AuthManager.change_password()
        elif choice == "9":
            if AuthManager.is_logged_in():
                save_students(registry)
            else:
                print("  ⛔  Please log in first.")
        elif choice == "L":
            if AuthManager.is_logged_in():
                AuthManager.logout()
            else:
                AuthManager.login()
        elif choice == "0":
            save_students(registry)
            print(f"\n  👋  Thank you for using {APP_NAME}. Goodbye!\n")
            break
        else:
            print("  ❌  Invalid option. Please try again.")

        if choice not in ("2", "3", "6", "7", "0"):
            input("\n  Press Enter to continue...")


# ══════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n  🚀  Starting {APP_NAME} v{VERSION} ...")
    load_students(registry)
    AuthManager.login()
    if AuthManager.is_logged_in():
        main_menu()
    else:
        print("  ⛔  Login failed. Exiting.")