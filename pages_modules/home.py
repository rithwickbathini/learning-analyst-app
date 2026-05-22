"""Home page: welcome screen with clickable quick-action cards."""
import streamlit as st


def _go(page_name: str):
    """Set the target page and rerun so the app navigates there."""
    st.session_state.go_to = page_name
    st.rerun()


def render():
    name = st.session_state.get("user_name", "there")

    st.title(f"👋 Welcome back, {name}!")
    st.markdown("#### Your learning platform — pick up where you left off.")
    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.markdown("### 📝 Take a Quiz")
            st.write("Test your Python & DSA knowledge with daily quizzes.")
            if st.button("Start Quiz", key="btn_quiz", use_container_width=True):
                _go("📝 Quizzes")

    with c2:
        with st.container(border=True):
            st.markdown("### 🎥 Watch Lessons")
            st.write("Learn from curated Python tutorial videos.")
            if st.button("Watch Now", key="btn_lessons", use_container_width=True):
                _go("🎥 Lessons")

    with c3:
        with st.container(border=True):
            st.markdown("### 📈 Track Scores")
            st.write("See your quiz history and watch your progress grow.")
            if st.button("View Scores", key="btn_scores", use_container_width=True):
                _go("📈 My Scores")

    st.divider()

    # A couple more quick links
    c4, c5 = st.columns(2)
    with c4:
        if st.button("🧩 Explore ServiceNow Classes", key="btn_snow", use_container_width=True):
            _go("🧩 ServiceNow")
    with c5:
        if st.button("📚 Browse All Courses", key="btn_courses", use_container_width=True):
            _go("📊 Dashboard")

    st.divider()
    st.markdown("#### How it works")
    st.markdown(
        """
        1. **Browse courses** and **watch lessons** to learn.
        2. **Take quizzes** to test yourself — basic to expert.
        3. **Check My Scores** to track your progress over time.
        4. Aim for **70%+** to pass each quiz!
        """
    )