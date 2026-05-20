"""Admin-only page: manage users from the database."""
import streamlit as st

from utils.db import get_db
from utils.ui_helpers import section_header


def render():
    section_header("🛠️ Admin Panel", "Manage users and platform settings")

    db = get_db()
    if db is None:
        st.error("Database not configured.")
        return

    users = db.table("users").select("email, name, role, created_at").execute().data

    c1, c2 = st.columns(2)
    c1.metric("Total Users", len(users))
    c2.metric("Admins", sum(1 for u in users if u["role"] == "admin"))

    st.markdown("#### Registered Users")
    if users:
        st.dataframe(users, use_container_width=True, hide_index=True)
    else:
        st.info("No users registered yet.")