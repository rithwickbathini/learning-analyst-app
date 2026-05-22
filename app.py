"""Main entry — handles auth, then routes by user role."""

import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- GRADIENT BACKGROUND ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #0F172A,
        #111827,
        #1E293B
    );
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD CUSTOM CSS ----------------
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("style.css file not found inside assets folder.")

# ---------------- IMPORT PAGES ----------------
from pages_modules import (
    home,
    dashboard,
    courses,
    servicenow,  # Added missing import to match the menu options
    lessons,
    quiz,
    my_scores,
    progress,
    upload_data,
    admin,
    ai_tutor,
    auth_page
)

# ---------------- IMPORT AUTH ----------------
from utils.auth import (
    is_authenticated,
    logout_user,
    current_role,
)

# ---------------- SESSION INIT ----------------
from utils.session_manager import init_session
init_session()

# ---------------- AUTH GATE ----------------
if not is_authenticated():
    auth_page.render()
    st.stop()

# ---------------- USER ROLE ----------------
role = current_role()

# ---------------- NAVIGATION STATE MANAGEMENT ----------------
# Handle inter-page programmatic redirection (e.g., clicking a button on Home to go to Courses)
if "go_to" in st.session_state:
    st.session_state.current_page = st.session_state.pop("go_to")

# Fallback initializer if session state is entirely blank
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# ---------------- DETERMINE MENUS BY ROLE ----------------
if role == "admin":
    options = [
        "🏠 Home",
        "📊 Dashboard",
        "📚 Courses",
        "🧩 ServiceNow",
        "🎥 Lessons",
        "📝 Quizzes",
        "📈 My Scores",
        "🎯 Progress",
        "📤 Upload Data",
        "🛠️ Admin Panel",
        "🤖 AI Tutor",
    ]
else:
    options = [
        "🏠 Home",
        "📊 Dashboard",
        "📚 Courses",
        "🧩 ServiceNow",
        "🎥 Lessons",
        "📝 Quizzes",
        "📈 My Scores",
        "🎯 Progress",
        "🤖 AI Tutor",
    ]

# Guard against role switching edge-cases causing IndexErrors
if st.session_state.current_page not in options:
    st.session_state.current_page = "🏠 Home"

# ---------------- SIDEBAR INTERFACE ----------------
with st.sidebar:
    st.title("🎓 LEARNING PLATFORM")
    st.caption(f"Welcome, {st.session_state.get('user_name', 'User')}")
    st.caption(f"Role: {role.capitalize()}")
    st.divider()

    # Tied directly to st.session_state["current_page"]
    page = st.radio(
        "Navigate",
        options,
        index=options.index(st.session_state.current_page),
        label_visibility="collapsed",
        key="current_page"
    )

    st.divider()

    # ---------------- LOGOUT ----------------
    if st.button("🚪 Logout", use_container_width=True):
        st.toast("Logged out successfully 👋")
        logout_user()
        st.rerun()

# ---------------- ROUTING ENGINE ----------------
if page == "🏠 Home":
    home.render()

elif page == "📊 Dashboard":
    dashboard.render()

elif page == "📚 Courses":
    courses.render()

elif page == "🧩 ServiceNow":
    servicenow.render()

elif page == "🎥 Lessons":
    lessons.render()

elif page == "📝 Quizzes":
    quiz.render()

elif page == "📈 My Scores":
    my_scores.render()

elif page == "🎯 Progress":
    progress.render()

elif page == "📤 Upload Data":
    if role == "admin":
        upload_data.render()
    else:
        st.error("Access denied. Admins only.")

elif page == "🛠️ Admin Panel":
    if role == "admin":
        admin.render()
    else:
        st.error("Access denied. Admins only.")

elif page == "🤖 AI Tutor":
    with st.spinner("Loading AI Tutor..."):
        ai_tutor.render()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2026 Learning Platform")