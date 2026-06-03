"""Profile page: view info, update name, change password."""
import streamlit as st

from utils.auth import current_email, current_role, change_password, update_user_name
from utils.db import get_db
from utils.ui_helpers import section_header


def render():
    section_header("👤 My Profile", "View and update your account")

    # Get info from session state first — always available
    email = st.session_state.get("user_email", "Not logged in")
    name = st.session_state.get("user_name", "Unknown")
    role = st.session_state.get("user_role", "student")

    # Try to get extra info (join date) from database
    joined = "N/A"
    db = get_db()
    if db is not None:
        try:
            result = db.table("users").select("created_at").eq("email", email).execute()
            if result.data and result.data[0].get("created_at"):
                joined = result.data[0]["created_at"][:10]
        except Exception:
            pass  # Silently skip — we already have the basics from session

    # --- Account info (always visible) ---
    st.markdown("#### Account Information")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Name**  \n{name}")
        c2.markdown(f"**Email**  \n{email}")
        c3.markdown(f"**Role**  \n{role.capitalize()}")
        st.caption(f"Member since: {joined}")

    st.divider()

    # --- Quick stats from session ---
    st.markdown("#### Quick Stats")
    with st.container(border=True):
        s1, s2 = st.columns(2)
        s1.metric("Account Type", role.capitalize())
        s2.metric("Status", "✅ Active")

    st.divider()

    # --- Update name ---
    st.markdown("#### Update Display Name")
    with st.form("update_name_form"):
        new_name = st.text_input("Your name", value=name)
        submitted = st.form_submit_button("💾 Save name", type="primary")
        if submitted:
            if db is None:
                st.error("Database not connected. Changes can't be saved right now.")
            else:
                ok, msg = update_user_name(email, new_name)
                st.success(msg) if ok else st.error(msg)
                if ok:
                    st.rerun()

    st.divider()

    # --- Change password ---
    st.markdown("#### Change Password")
    with st.form("change_password_form"):
        current_pw = st.text_input("Current password", type="password")
        new_pw = st.text_input("New password (min 6 characters)", type="password")
        confirm_pw = st.text_input("Confirm new password", type="password")
        submitted_pw = st.form_submit_button("🔒 Change password", type="primary")
        if submitted_pw:
            if db is None:
                st.error("Database not connected. Password can't be changed right now.")
            elif new_pw != confirm_pw:
                st.error("New passwords do not match.")
            else:
                ok, msg = change_password(email, current_pw, new_pw)
                st.success(msg) if ok else st.error(msg)