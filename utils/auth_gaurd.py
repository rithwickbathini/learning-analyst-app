import streamlit as st

from utils.auth import is_authenticated, current_role


def require_login():
    if not is_authenticated():
        st.error("Please login first.")
        st.stop()


def require_admin():
    require_login()

    if current_role() != "admin":
        st.error("Access denied.")
        st.stop()