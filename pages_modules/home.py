"""Home page: welcome screen with quick links and an overview."""
import streamlit as st


def render():
    name = st.session_state.get("user_name", "there")

    st.title(f"👋 Welcome back, {name}!")
    st.markdown("#### Your learning platform — pick up where you left off.")
    st.divider()

    # Quick-start cards
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("### 📝 Take a Quiz")
            st.write("Test your Python & DSA knowledge with daily quizzes.")
            st.caption("Go to **📝 Quizzes** in the sidebar.")
    with c2:
        with st.container(border=True):
            st.markdown("### 🎥 Watch Lessons")
            st.write("Learn from curated Python tutorial videos.")
            st.caption("Go to **🎥 Lessons** in the sidebar.")
    with c3:
        with st.container(border=True):
            st.markdown("### 📈 Track Scores")
            st.write("See your quiz history and watch your progress grow.")
            st.caption("Go to **📈 My Scores** in the sidebar.")

    st.divider()

    st.markdown("#### How it works")
    st.markdown(
        """
        1. **Browse courses** and **watch lessons** to learn.
        2. **Take quizzes** to test yourself — 10 questions a day, basic to expert.
        3. **Check My Scores** to track your progress over time.
        4. Aim for **70%+** to pass each quiz!
        """
    )
    st.markdown("---")
    st.caption("© 2026 Learning Platform")