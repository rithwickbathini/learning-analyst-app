"""Authentication backed by Supabase (PostgreSQL). Accounts persist forever."""
import bcrypt
import streamlit as st

from utils.db import get_db


def _hash_password(plain: str) -> str:
    """Turn a plain password into a secure hash for storage."""
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def _check_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a stored hash."""
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def register_user(email: str, name: str, password: str, role: str = "student"):
    """Create a new account in the database. Returns (success, message)."""
    email = email.strip().lower()
    if not email or not name or not password:
        return False, "All fields are required."
    if "@" not in email:
        return False, "Please enter a valid email."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    db = get_db()
    if db is None:
        return False, "Database not configured. Check your Supabase keys."

    # Check if email already exists
    existing = db.table("users").select("email").eq("email", email).execute()
    if existing.data:
        return False, "An account with this email already exists."

    db.table("users").insert({
        "email": email,
        "name": name,
        "password_hash": _hash_password(password),
        "role": role,
    }).execute()
    return True, "Account created! You can now log in."


def login_user(email: str, password: str):
    """Validate credentials against the database. Returns (success, message)."""
    email = email.strip().lower()
    db = get_db()
    if db is None:
        return False, "Database not configured. Check your Supabase keys."

    result = db.table("users").select("*").eq("email", email).execute()
    if not result.data:
        return False, "No account found with this email."

    user = result.data[0]
    if not _check_password(password, user["password_hash"]):
        return False, "Incorrect password."

    st.session_state.authenticated = True
    st.session_state.user_email = user["email"]
    st.session_state.user_name = user["name"]
    st.session_state.user_role = user["role"]
    return True, "Logged in successfully."


def logout_user():
    """Clear the session, logging the user out."""
    for key in ["authenticated", "user_email", "user_name", "user_role"]:
        st.session_state.pop(key, None)


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def current_role() -> str:
    return st.session_state.get("user_role", "")


def current_email() -> str:
    return st.session_state.get("user_email", "")