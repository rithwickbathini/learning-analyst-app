"""Lessons page: Course tutorial videos."""

import streamlit as st
from utils.ui_helpers import section_header


# ---------------- LESSON LIBRARY ----------------
LESSONS_LIBRARY = {

    "python": {
        "course_name": "Python Programming",
        "videos": [
            {
                "title": "Python Full Course for Beginners",
                "description": "A complete introduction to Python programming.",
                "level": "Beginner",
                "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
            },
            {
                "title": "Python in 100 Seconds",
                "description": "Quick overview of Python.",
                "level": "Beginner",
                "url": "https://www.youtube.com/watch?v=x7X9w_GIm1s",
            },
            {
                "title": "Object-Oriented Programming",
                "description": "Classes and OOP concepts.",
                "level": "Intermediate",
                "url": "https://www.youtube.com/watch?v=Ej_02ICOIgs",
            },
        ],
    },

    "streamlit": {
        "course_name": "Streamlit Apps",
        "videos": [
            {
                "title": "Streamlit Full Tutorial",
                "description": "Build interactive dashboards using Streamlit.",
                "level": "Beginner",
                "url": "https://www.youtube.com/watch?v=B0MUXbXQreY",
            }
        ],
    },
}


# ---------------- RENDER ----------------
def render():

    # Get selected course from Courses page
    current_course = st.session_state.get(
        "selected_course"
    )

    # Safe fallback
    if not current_course or current_course not in LESSONS_LIBRARY:

        st.warning(
            "No course selected. Showing Python track."
        )

        current_course = "python"

    course_data = LESSONS_LIBRARY[current_course]
    lessons = course_data["videos"]

    # ---------------- HEADER ----------------
    section_header(
        f"🎥 {course_data['course_name']} Lessons",
        "Watch tutorial videos and learn step-by-step"
    )

    st.divider()

    # ---------------- FILTER ----------------
    levels = ["All"] + sorted(
        list(
            {
                lesson["level"]
                for lesson in lessons
            }
        )
    )

    selected_level = st.selectbox(
        "📊 Filter Difficulty",
        levels
    )

    # Apply filter
    if selected_level == "All":
        visible_lessons = lessons
    else:
        visible_lessons = [
            lesson
            for lesson in lessons
            if lesson["level"] == selected_level
        ]

    st.caption(
        f"{len(visible_lessons)} lessons available"
    )

    # No lessons
    if not visible_lessons:
        st.info(
            "No lessons available for this level."
        )
        return

    st.divider()

    # ---------------- VIDEO CARDS ----------------
    for lesson in visible_lessons:

        with st.container(border=True):

            st.markdown(
                f"### 🎬 {lesson['title']}"
            )

            st.caption(
                f"📊 {lesson['level']}"
            )

            st.write(
                lesson["description"]
            )

            st.video(
                lesson["url"]
            )

            st.link_button(
                "▶ Open in YouTube",
                lesson["url"],
                use_container_width=True
            )