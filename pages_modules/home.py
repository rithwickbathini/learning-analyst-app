"""Home page: welcome screen with clickable quick-action cards."""

import streamlit as st
from streamlit_lottie import st_lottie

def _go(page_name: str):
    """Navigate to another page."""
    st.session_state.go_to = page_name
    st.rerun()


def render():

    name = st.session_state.get("user_name", "there")

    # ---------------- HERO + LOTTIE----------------

    st.title(f"👋 Welcome back, {name}!")
    col1, col2 = st.columns([2, 1])
    st.markdown(
        """
        ### 🚀 Your AI-Powered Learning Platform

        Learn Python, DSA, and ServiceNow with:
        - 🎥 Interactive lessons
        - 📝 Smart quizzes
        - 📈 Progress tracking
        - 🤖 AI Tutor assistance
        - 🧩 Real-world projects
        """
    )
    with col1:
        st.title("🚀 Smart Learning Platform")
        st.markdown("""
                Learn ServiceNow, analytics, development,
                and AI-powered workflows in one place.
                """)

    with col2:
        animation = st.session_state.get("lottie_learning")

        if animation is not None:
            st_lottie(
                animation,
                height=180,
                key="learning_anim"
            )
        else:
            st.info("🎓 Learning Platform")

    st.divider()

    # ---------------- METRICS ----------------
    st.subheader("📈 Platform KPIs")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Active Learners",
            "1,248",
            "+12%"
        )

    with c2:
        st.metric(
            "Completion Rate",
            "78%",
            "+5%"
        )

    with c3:
        st.metric(
            "Study Hours",
            "4,820",
            "+18%"
        )

    with c4:
        st.metric(
            "Satisfaction",
            "4.8/5",
            "Stable"
        )

    st.divider()

    # ---------------- QUICK ACTION CARDS ----------------
    col1, col2, col3 = st.columns(3)

    # QUIZ CARD
    with col1:

        with st.container(border=True):

            st.markdown("## 📝 Take a Quiz")

            st.write(
                "Test your Python, DSA, and ServiceNow skills with interactive quizzes."
            )

            st.write("✔ Beginner to Advanced")

            st.write("✔ Instant scoring")

            st.write("✔ Performance tracking")

            if st.button(
                "Start Quiz",
                key="btn_quiz",
                use_container_width=True
            ):

                _go("📝 Quizzes")

    # LESSONS CARD
    with col2:

        with st.container(border=True):

            st.markdown("## 🎥 Watch Lessons")

            st.write(
                "Learn from curated video tutorials and practical coding sessions."
            )

            st.write("✔ Python")

            st.write("✔ DSA")

            st.write("✔ ServiceNow")

            if st.button(
                "Watch Lessons",
                key="btn_lessons",
                use_container_width=True
            ):

                _go("🎥 Lessons")

    # SCORES CARD
    with col3:

        with st.container(border=True):

            st.markdown("## 📈 Track Progress")

            st.write(
                "Monitor quiz scores, completed lessons, and learning analytics."
            )

            st.write("✔ Score history")

            st.write("✔ Growth analytics")

            st.write("✔ Learning insights")

            if st.button(
                "View Progress",
                key="btn_scores",
                use_container_width=True
            ):

                _go("📈 My Scores")

    st.divider()

    # ---------------- SECOND ROW ----------------
    c4, c5 = st.columns(2)

    # SERVICENOW
    with c4:

        with st.container(border=True):

            st.markdown("## 🧩 ServiceNow Learning")

            st.write(
                "Master ServiceNow from basics to advanced development concepts."
            )

            st.write("✔ Client Scripts")

            st.write("✔ Business Rules")

            st.write("✔ Workflows")

            st.write("✔ Integrations")

            if st.button(
                "Explore ServiceNow",
                key="btn_snow",
                use_container_width=True
            ):

                _go("🧩 ServiceNow")

    # COURSES
    with c5:

        with st.container(border=True):

            st.markdown("## 📚 Browse Courses")

            st.write(
                "Access all available learning paths and structured roadmaps."
            )

            st.write("✔ Beginner Friendly")

            st.write("✔ Career Focused")

            st.write("✔ Practical Projects")

            if st.button(
                "Browse Courses",
                key="btn_courses",
                use_container_width=True
            ):

                _go("📚 Courses")

    st.divider()

    # ---------------- HOW IT WORKS ----------------
    st.markdown("## ⚡ How It Works")

    st.markdown(
        """
        ### Step 1 — Learn
        Browse courses and watch structured lessons.

        ### Step 2 — Practice
        Take quizzes and solve coding challenges.

        ### Step 3 — Track
        Monitor your performance and growth.

        ### Step 4 — Improve
        Use the AI Tutor and ServiceNow labs to level up.

        ### Step 5 — Become Job Ready
        Build real-world skills for internships and placements.
        """
    )

    st.divider()

    # ---------------- MOTIVATION ----------------
    st.success(
        "🔥 Consistency beats intensity — learn something every day."
    )