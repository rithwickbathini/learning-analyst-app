import bcrypt
import streamlit as st
import requests
from streamlit_lottie import st_lottie
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

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
def update_user_name(email: str, new_name: str):
    """Update the user's display name. Returns (success, message)."""
    new_name = new_name.strip()
    if not new_name:
        return False, "Name cannot be empty."

    db = get_db()
    if db is None:
        return False, "Database not configured."

    try:
        db.table("users").update({"name": new_name}).eq("email", email).execute()
        st.session_state.user_name = new_name  # Reflect change immediately
        return True, "Name updated successfully."
    except Exception:
        return False, "Could not reach the database. Please try again."


def change_password(email: str, current_password: str, new_password: str):
    """Verify current password, then set a new one. Returns (success, message)."""
    if not current_password or not new_password:
        return False, "All fields are required."
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters."

    db = get_db()
    if db is None:
        return False, "Database not configured."

    # 1) Fetch current hash
    try:
        result = db.table("users").select("password_hash").eq("email", email).execute()
    except Exception:
        return False, "Could not reach the database. Please try again."

    if not result.data:
        return False, "Account not found."

    # 2) Verify current password
    if not _check_password(current_password, result.data[0]["password_hash"]):
        return False, "Current password is incorrect."

    # 3) Save new hashed password
    try:
        db.table("users").update({
            "password_hash": _hash_password(new_password)
        }).eq("email", email).execute()
        return True, "Password changed successfully."
    except Exception:
        return False, "Could not reach the database. Please try again."