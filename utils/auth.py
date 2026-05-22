import bcrypt
import streamlit as st

from utils.db import get_db


# ---------------- PASSWORD HELPERS ----------------

def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(
        plain.encode(),
        bcrypt.gensalt()
    ).decode()


def _check_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode(),
        hashed.encode()
    )


# ---------------- REGISTER USER ----------------

def register_user(
    email: str,
    name: str,
    password: str,
    role: str = "student",
):
    email = email.strip().lower()

    if not email or not name or not password:
        return False, "All fields are required."

    if "@" not in email:
        return False, "Please enter a valid email."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    db = get_db()

    if db is None:
        return False, "Database not configured."

    # Check existing user
    existing = (
        db.table("users")
        .select("email")
        .eq("email", email)
        .execute()
    )

    if existing.data:
        return False, "Account already exists."

    # Insert new user
    db.table("users").insert({
        "email": email,
        "name": name,
        "password_hash": _hash_password(password),
        "role": role,
    }).execute()

    return True, "Account created successfully."


# ---------------- LOGIN USER ----------------

def login_user(email: str, password: str):
    email = email.strip().lower()

    db = get_db()

    if db is None:
        return False, "Database not configured."

    result = (
        db.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not result.data:
        return False, "No account found."

    user = result.data[0]

    if not _check_password(
        password,
        user["password_hash"]
    ):
        return False, "Incorrect password."

    # Session state
    st.session_state.authenticated = True
    st.session_state.user_email = user["email"]
    st.session_state.user_name = user["name"]
    st.session_state.user_role = user["role"]

    # Login toast
    st.toast("Login successful ✅")

    return True, "Logged in successfully."


# ---------------- LOGOUT ----------------

def logout_user():
    """Clear session data."""

    for key in [
        "authenticated",
        "user_email",
        "user_name",
        "user_role",
    ]:
        st.session_state.pop(key, None)


# ---------------- SESSION HELPERS ----------------

def is_authenticated() -> bool:
    return st.session_state.get(
        "authenticated",
        False
    )


def current_role() -> str:
    return st.session_state.get(
        "user_role",
        ""
    )


def current_email() -> str:
    return st.session_state.get(
        "user_email",
        ""
    )