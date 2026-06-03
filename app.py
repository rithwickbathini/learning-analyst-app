"""Main entry — handles auth, then routes by user role."""

# ---------------- IMPORTS ----------------
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit_lottie import st_lottie

# ---------------- LOTTIE LOADER ----------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
             return r.json()
        return None

    except Exception as e:
        print("Lottie load failed:", e)
        return None


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- GLOBAL UI ----------------
st.markdown("""
<style>

/* APP BACKGROUND */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 1rem;
    max-width: 1450px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    height: 48px;
    border: none;
    border-radius: 12px;
    background-color: #6366f1;
    color: white;
    font-weight: 600;
}

/* BUTTON HOVER */
.stButton > button:hover {
    background-color: #4f46e5;
}

/* INPUTS */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #0b1220 !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #374151 !important;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] {
    background-color: #0b1220 !important;
    color: white !important;
    border-radius: 10px !important;
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background-color: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* IMAGES */
img {
    max-width: 100%;
    border-radius: 10px;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background-color: #6366f1;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- IMPORT PAGES ----------------
from pages_modules import (
    home,
    dashboard,
    servicenow,
    lessons,
    quiz,
    my_scores,
    progress,
    upload_data,
    admin,
    ai_tutor,
    auth_page,
    profile
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

# ---------------- LOTTIE ANIMATION ----------------
lottie_learning = load_lottieurl(
    "https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json"
)

# ---------------- STORE LOTTIE IN SESSION ----------------
st.session_state.lottie_learning = lottie_learning

# ---------------- AUTH GATE ----------------
if not is_authenticated():
    auth_page.render()
    st.stop()

# ---------------- USER ROLE ----------------
role = current_role()

# ---------------- PAGE STATE ----------------
if "go_to" in st.session_state:
    st.session_state.current_page = st.session_state.pop("go_to")

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# ---------------- HERO SECTION ----------------
if st.session_state.current_page == "🏠 Home":

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.title("🎓 AI Learning Platform")

        st.markdown("""
### Learn ServiceNow from Beginner to Advanced

✔ Interactive Lessons  
✔ AI Tutor  
✔ Real Progress Tracking  
✔ Smart Quizzes  
✔ Career Growth Roadmaps  
✔ Hands-on Projects
""")

        st.info(
            "🚀 Start your ServiceNow journey and become job-ready."
        )

    with col2:

        if st.session_state.lottie_learning:

            st_lottie(
                st.session_state.lottie_learning,
                height=280,
                key="learning_animation"
            )

    st.markdown("---")

# ---------------- MENU OPTIONS ----------------
if role == "admin":

    options = [
        "🏠 Home",
        "📊 Dashboard",
        "🧩 ServiceNow",
        "🎥 Lessons",
        "📝 Quizzes",
        "📈 My Scores",
        "🎯 Progress",
        "👤Profile",
        "📤 Upload Data",
        "🛠️ Admin Panel",
        "🤖 AI Tutor",
    ]

else:

    options = [
        "🏠 Home",
        "📊 Dashboard",
        "🧩 ServiceNow",
        "🎥 Lessons",
        "📝 Quizzes",
        "📈 My Scores",
        "🎯 Progress",
        "🤖 AI Tutor",
        "👤Profile",
    ]

# ---------------- SAFE PAGE CHECK ----------------
if st.session_state.current_page not in options:
    st.session_state.current_page = "🏠 Home"

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("🎓 LEARNING PLATFORM")

    st.caption(
        f"Welcome, {st.session_state.get('user_name', 'User')}"
    )

    st.caption(
        f"Role: {role.capitalize()}"
    )

    st.divider()

    page = st.radio(
        "Navigate",
        options,
        index=options.index(
            st.session_state.current_page
        ),
        label_visibility="collapsed",
        key="current_page"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.toast(
            "Logged out successfully 👋"
        )

        logout_user()
        st.rerun()

# ---------------- ROUTING ----------------
if page == "🏠 Home":
    with st.spinner("Loading Home..."):
        home.render()

if page == "👤 Profile":
    with st.spinner("Loading Profile..."):
        profile.render()

elif page == "📊 Dashboard":
    with st.spinner("Loading Dashboard..."):
        dashboard.render()

elif page == "🧩 ServiceNow":
    with st.spinner("Loading ServiceNow..."):
        servicenow.render()

elif page == "🎥 Lessons":
    with st.spinner("Loading Lessons..."):
        lessons.render()

elif page == "📝 Quizzes":
    with st.spinner("Loading Quizzes..."):
        quiz.render()

elif page == "📈 My Scores":
    with st.spinner("Loading Scores..."):
        my_scores.render()

elif page == "🎯 Progress":
    with st.spinner("Loading Progress..."):
        progress.render()

elif page == "📤 Upload Data":

    if role == "admin":
        with st.spinner("Loading Upload Data..."):
            upload_data.render()
    else:
        st.error(
            "Access denied. Admins only."
        )

elif page == "🛠️ Admin Panel":

    if role == "admin":
        with st.spinner("Loading Admin Panel..."):
            admin.render()
    else:
        st.error(
            "Access denied. Admins only."
        )

elif page == "🤖 AI Tutor":

    with st.spinner(
        "Loading AI Tutor..."
    ):
        ai_tutor.render()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2026 Learning Platform")