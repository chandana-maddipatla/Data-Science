
from utils import (
    validate_name, validate_student_id, validate_age,
    validate_grade, validate_email, grade_to_letter, grade_to_status
)


# ──────────────────────────────────────────────
# Student  (Entity class)
# ──────────────────────────────────────────────

class Student:
    """Represents a single student record."""

    # Class-level counter used to auto-generate IDs when needed
    _id_counter: int = 1

    def __init__(
        self,
        name: str,
        age: int,
        course: str,
        grade: float,
        email: str,
        student_id: str = "",
    ) -> None:
        self.student_id: str  = student_id or Student._next_id()
        self.name: str        = name
        self.age: int         = int(age)
        self.course: str      = course
        self.grade: float     = float(grade)
        self.email: str       = email

    # ── Auto-ID helper ──────────────────────────
    @classmethod
    def _next_id(cls) -> str:
        sid = f"STU{cls._id_counter:03d}"
        cls._id_counter += 1
        return sid

    # ── Properties with validation ──────────────
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not validate_name(value):
            raise ValueError(f"Invalid name: '{value}'. Use letters and spaces only (min 2 chars).")
        self._name = value.strip().title()

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value) -> None:
        if not validate_age(str(value)):
            raise ValueError(f"Invalid age: {value}. Must be between 5 and 100.")
        self._age = int(value)

    @property
    def grade(self) -> float:
        return self._grade

    @grade.setter
    def grade(self, value) -> None:
        if not validate_grade(str(value)):
            raise ValueError(f"Invalid grade: {value}. Must be between 0.0 and 100.0.")
        self._grade = float(value)

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not validate_email(value):
            raise ValueError(f"Invalid email: '{value}'.")
        self._email = value.strip().lower()

    # ── Serialisation ───────────────────────────
    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name":       self.name,
            "age":        self.age,
            "course":     self.course,
            "grade":      self.grade,
            "email":      self.email,
        }

    def to_file_line(self) -> str:
        """Pipe-delimited string for flat-file storage."""
        d = self.to_dict()
        return "|".join(str(v) for v in d.values())

    @staticmethod
    def from_file_line(line: str) -> "Student":
        """Reconstruct a Student from a pipe-delimited file line."""
        parts = line.strip().split("|")
        if len(parts) != 6:
            raise ValueError(f"Malformed record: {line!r}")
        sid, name, age, course, grade, email = parts
        return Student(
            name=name,
            age=int(age),
            course=course,
            grade=float(grade),
            email=email,
            student_id=sid,
        )

    # ── Display ─────────────────────────────────
    def __str__(self) -> str:
        letter = grade_to_letter(self.grade)
        status = grade_to_status(self.grade)
        return (
            f"  ID      : {self.student_id}\n"
            f"  Name    : {self.name}\n"
            f"  Age     : {self.age}\n"
            f"  Course  : {self.course}\n"
            f"  Grade   : {self.grade:.1f}  ({letter})  [{status}]\n"
            f"  Email   : {self.email}"
        )

    def __repr__(self) -> str:
        return f"Student(id={self.student_id!r}, name={self.name!r}, grade={self.grade})"


# ──────────────────────────────────────────────
# StudentRegistry  (in-memory data structure)
# ──────────────────────────────────────────────

class StudentRegistry:
   

    def __init__(self) -> None:
        self._students: list[Student]       = []
        self._index:    dict[str, Student]  = {}

    # ── CRUD ────────────────────────────────────
    def add(self, student: Student) -> None:
        if student.student_id in self._index:
            raise ValueError(f"Student ID '{student.student_id}' already exists.")
        self._students.append(student)
        self._index[student.student_id] = student

    def get_by_id(self, student_id: str) -> Student | None:
        return self._index.get(student_id.upper())

    def search_by_name(self, query: str) -> list[Student]:
        q = query.lower()
        return [s for s in self._students if q in s.name.lower()]

    def search_by_course(self, course: str) -> list[Student]:
        c = course.lower()
        return [s for s in self._students if c in s.course.lower()]

    def delete(self, student_id: str) -> Student | None:
        student = self._index.pop(student_id.upper(), None)
        if student:
            self._students.remove(student)
        return student

    def update(self, student_id: str, **fields) -> Student | None:
        student = self.get_by_id(student_id)
        if not student:
            return None
        for key, value in fields.items():
            if hasattr(student, key):
                setattr(student, key, value)
        return student

    # ── Convenience ─────────────────────────────
    def all(self) -> list[Student]:
        return list(self._students)

    def count(self) -> int:
        return len(self._students)

    def clear(self) -> None:
        self._students.clear()
        self._index.clear()

    def load(self, students: list[Student]) -> None:
        """Bulk-load students (e.g. from file). Resets registry first."""
        self.clear()
        for s in students:
            self._students.append(s)
            self._index[s.student_id] = s
        # Sync auto-ID counter so new IDs don't clash
        if students:
            max_num = 0
            for s in students:
                try:
                    max_num = max(max_num, int(s.student_id[3:]))
                except ValueError:
                    pass
            Student._id_counter = max_num + 1

    def statistics(self) -> dict:
        if not self._students:
            return {}
        grades = [s.grade for s in self._students]
        return {
            "total":   self.count(),
            "average": round(sum(grades) / len(grades), 2),
            "highest": max(grades),
            "lowest":  min(grades),
            "passing": sum(1 for g in grades if g >= 50),
            "failing": sum(1 for g in grades if g < 50),
        }
