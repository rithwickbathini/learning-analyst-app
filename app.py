"""Main entry — handles auth, then routes by user role."""
import streamlit as st

from pages_modules import dashboard, courses, progress, upload_data, auth_page, admin, lessons, quiz, my_scores
from utils.auth import is_authenticated, logout_user, current_role

st.set_page_config(
    page_title="Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Gate: if not logged in, show only the login screen ---
if not is_authenticated():
    auth_page.render()
    st.stop()  # Stop here — nothing below runs until logged in

# --- Logged in: build sidebar based on role ---
role = current_role()

with st.sidebar:
    st.title("🎓 Learning Platform")
    st.caption(f"Welcome, {st.session_state.get('user_name', 'User')}")
    st.caption(f"Role: {role.capitalize()}")
    st.divider()

    # Students and admins see different menus
    if role == "admin":
        options = ["📊 Dashboard", "📚 Courses", "🎥 Lessons", "📝 Quizzes", "📈 My Scores", "🎯 Progress", "📤 Upload Data", "🛠️ Admin Panel"]
    else:
        options = ["📊 Dashboard", "📚 Courses", "🎥 Lessons", "📝 Quizzes", "📈 My Scores", "🎯 Progress"]

    page = st.radio("Navigate", options, label_visibility="collapsed")

    st.divider()
    if st.button("🚪 Logout"):
        logout_user()
        st.rerun()

# --- Route to the chosen page ---
if page == "📊 Dashboard":
    dashboard.render()
elif page == "📚 Courses":
    courses.render()
elif page == "🎥 Lessons":
    lessons.render()
elif page == "📝 Quizzes":
    quiz.render()
elif page == "📈 My Scores":
    my_scores.render()
elif page == "🎯 Progress":
    progress.render()
elif page == "📤 Upload Data":
    upload_data.render()
elif page == "🛠️ Admin Panel":
    # Extra safety: double-check role before rendering admin content
    if role == "admin":
        admin.render()
    else:
        st.error("Access denied. Admins only.")