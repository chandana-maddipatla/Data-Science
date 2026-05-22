"""
auth.py — Authentication module for the Student Management System.

Covers:
    - dotenv usage (admin credentials stored in .env)
    - Session state management
    - Exception handling for auth errors
"""

import os
import hashlib
from dotenv import load_dotenv
from decorators import logger

# Load environment variables from .env
load_dotenv()

_ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
_ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")


def _hash(password: str) -> str:
    """SHA-256 hash a password string."""
    return hashlib.sha256(password.encode()).hexdigest()


# Pre-hash the stored password for comparison
_HASHED_PASSWORD: str = _hash(_ADMIN_PASSWORD)


class AuthManager:
    """
    Singleton-style auth manager.
    Uses a class variable to track login state across modules.
    """

    _logged_in: bool = False
    _current_user: str = ""

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls._logged_in

    @classmethod
    def current_user(cls) -> str:
        return cls._current_user

    @classmethod
    @logger
    def login(cls) -> bool:
        """Prompt for credentials and authenticate."""
        print("\n" + "=" * 40)
        print("        🔐  ADMIN LOGIN")
        print("=" * 40)

        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                username = input("  Username : ").strip()
                password = input("  Password : ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n  Login cancelled.")
                return False

            if username == _ADMIN_USERNAME and _hash(password) == _HASHED_PASSWORD:
                cls._logged_in  = True
                cls._current_user = username
                print(f"\n  ✅  Welcome, {username}! Login successful.\n")
                return True
            else:
                remaining = max_attempts - attempt
                if remaining > 0:
                    print(f"  ❌  Invalid credentials. {remaining} attempt(s) remaining.\n")
                else:
                    print("  ❌  Too many failed attempts. Access blocked.\n")

        return False

    @classmethod
    def logout(cls) -> None:
        cls._logged_in   = False
        cls._current_user = ""
        print("\n  👋  Logged out successfully.\n")

    @classmethod
    def change_password(cls) -> None:
        """Allow the logged-in admin to change the in-session password hash."""
        if not cls._logged_in:
            print("  ⛔  You must be logged in to change the password.")
            return
        try:
            old_pw  = input("  Current password : ").strip()
            new_pw  = input("  New password     : ").strip()
            confirm = input("  Confirm new      : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Change cancelled.")
            return

        global _HASHED_PASSWORD
        if _hash(old_pw) != _HASHED_PASSWORD:
            print("  ❌  Incorrect current password.")
            return
        if new_pw != confirm:
            print("  ❌  New passwords do not match.")
            return
        if len(new_pw) < 6:
            print("  ❌  Password must be at least 6 characters.")
            return

        _HASHED_PASSWORD = _hash(new_pw)
        print("  ✅  Password changed successfully (session only).")
        print("  ℹ️   Update your .env file to make the change permanent.")
