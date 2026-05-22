import streamlit as st

from utils.auth_guard import require_admin

require_admin()

st.title("Admin Dashboard")

st.success("Welcome Admin")