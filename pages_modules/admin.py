"""Admin-only page: manage users and view system info."""
import json

import streamlit as st

from utils.auth import USERS_FILE
from utils.ui_helpers import section_header


def render():
    section_header("🛠️ Admin Panel", "Manage users and platform settings")

    # Load users to display (without showing password hashes)
    if USERS_FILE.exists():
        with open(USERS_FILE) as f:
            users = json.load(f)
    else:
        users = {}

    c1, c2 = st.columns(2)
    c1.metric("Total Users", len(users))
    c2.metric("Admins", sum(1 for u in users.values() if u["role"] == "admin"))

    st.markdown("#### Registered Users")
    rows = [
        {"Email": email, "Name": data["name"], "Role": data["role"]}
        for email, data in users.items()
    ]
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No users registered yet.")

    st.info("This is an admin-only area. Students cannot see this page.")