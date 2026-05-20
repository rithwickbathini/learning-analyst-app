"""Simple authentication: login, signup, roles, password hashing.

NOTE: Users are stored in users.json. On Streamlit Cloud's free tier this
file resets when the app restarts. For permanent storage you need a real
database (PostgreSQL). This is suitable for learning and demos.
"""
import json
from pathlib import Path

import bcrypt
import streamlit as st

USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"


def _load_users() -> dict:
    """Read all users from the JSON file."""
    if not USERS_FILE.exists():
        # Seed with one default admin on first run
        default = {
            "admin@app.com": {
                "name": "Administrator",
                "password": _hash_password("admin123"),
                "role": "admin",
            }
        }
        _save_users(default)
        return default
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def _save_users(users: dict) -> None:
    """Write all users to the JSON file."""
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def _hash_password(plain: str) -> str:
    """Turn a plain password into a secure hash for storage."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def _check_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a stored hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def register_user(email: str, name: str, password: str, role: str = "student") -> tuple[bool, str]:
    """Create a new account. Returns (success, message)."""
    email = email.strip().lower()
    if not email or not name or not password:
        return False, "All fields are required."
    if "@" not in email:
        return False, "Please enter a valid email."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    users = _load_users()
    if email in users:
        return False, "An account with this email already exists."

    users[email] = {"name": name, "password": _hash_password(password), "role": role}
    _save_users(users)
    return True, "Account created! You can now log in."


def login_user(email: str, password: str) -> tuple[bool, str]:
    """Validate credentials and set session state. Returns (success, message)."""
    email = email.strip().lower()
    users = _load_users()

    if email not in users:
        return False, "No account found with this email."
    if not _check_password(password, users[email]["password"]):
        return False, "Incorrect password."

    # Store the logged-in user in the session
    st.session_state.authenticated = True
    st.session_state.user_email = email
    st.session_state.user_name = users[email]["name"]
    st.session_state.user_role = users[email]["role"]
    return True, "Logged in successfully."


def logout_user() -> None:
    """Clear the session, logging the user out."""
    for key in ["authenticated", "user_email", "user_name", "user_role"]:
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def current_role() -> str:
    return st.session_state.get("user_role", "")