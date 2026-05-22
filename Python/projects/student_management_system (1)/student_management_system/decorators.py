"""
decorators.py — Reusable decorators for the Student Management System.

Covers:
    - Logging decorator  (writes timestamped entries to activity.log)
    - Validation decorator (ensures the user is authenticated before calling a function)
    - Timer decorator     (measures execution time — useful for report generation)
"""

import os
import time
import functools
from datetime import datetime


# ──────────────────────────────────────────────
# 1.  Logger decorator
# ──────────────────────────────────────────────
LOG_FILE = os.getenv("LOG_FILE", "activity.log")


def logger(func):
    """Log every call to *func* (name + timestamp + outcome) to LOG_FILE."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            result = func(*args, **kwargs)
            status = "SUCCESS"
        except Exception as exc:
            status = f"FAILED ({exc})"
            result = None
            raise
        finally:
            log_entry = f"[{timestamp}] {func.__name__} → {status}\n"
            try:
                with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                    log_file.write(log_entry)
            except OSError:
                pass  # Never let logging crash the application
        return result

    return wrapper


# ──────────────────────────────────────────────
# 2.  Auth-required decorator
# ──────────────────────────────────────────────
def require_auth(func):
    """Block execution if the session is not authenticated."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Import here to avoid a circular import
        from auth import AuthManager
        if not AuthManager.is_logged_in():
            print("\n⛔  Access denied. Please log in first.\n")
            return None
        return func(*args, **kwargs)

    return wrapper


# ──────────────────────────────────────────────
# 3.  Timer decorator
# ──────────────────────────────────────────────
def timer(func):
    """Print how long *func* took to execute."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱  '{func.__name__}' completed in {elapsed:.4f}s")
        return result

    return wrapper
