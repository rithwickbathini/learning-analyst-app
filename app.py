"""Main entry point — AI Learning Platform with sidebar navigation."""
import streamlit as st

from pages_modules import dashboard, courses, progress, upload_data

st.set_page_config(
    page_title="Learning Analytics Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("🎓 Learning Analytics")
    st.caption("Course performance dashboard")
    st.divider()

    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "📚 Courses", "🎯 My Progress", "📤 Upload Data"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Built with Streamlit")

if page == "📊 Dashboard":
    dashboard.render()
elif page == "📚 Courses":
    courses.render()
elif page == "🎯 My Progress":
    progress.render()
elif page == "📤 Upload Data":
    upload_data.render()