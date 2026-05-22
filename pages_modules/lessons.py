"""Lessons page: Python tutorial videos."""

import streamlit as st
from utils.ui_helpers import section_header

# Organized by course key to allow cross-page dynamic navigation
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
                "description": "A lightning-fast overview of what Python is.",
                "level": "Beginner",
                "url": "https://www.youtube.com/watch?v=x7X9w_GIm1s",
            },
            {
                "title": "Object-Oriented Programming in Python",
                "description": "Learn classes, objects, and inheritance.",
                "level": "Intermediate",
                "url": "https://www.youtube.com/watch?v=Ej_02ICOIgs",
            },
            {
                "title": "Python Data Structures",
                "description": "Lists, dictionaries, sets, and tuples explained.",
                "level": "Intermediate",
                "url": "https://www.youtube.com/watch?v=R-HLU9Fl5ug",
            },
        ],
    },
    "streamlit": {
        "course_name": "Streamlit Apps",
        "videos": [
            {
                "title": "Streamlit Full Tutorial",
                "description": "Build your first interactive web dashboard.",
                "level": "Beginner",
                "url": "https://www.youtube.com/watch?v=B0MUXbXQreY",
            }
        ],
    },
}


def render():
    # 1. Check if a specific course was selected from the Courses Page
    current_course_key = st.session_state.get("current_course", None)

    # If nothing is in state, show an optional info box rather than crashing,
    # but still let them pick something to view right away!
    if not current_course_key or current_course_key not in LESSONS_LIBRARY:
        st.info("💡 Tip: You can jump straight to a track by clicking 'Continue Learning' on the Courses page!")
        current_course_key = "python"  # Clean fallback default

    course_data = LESSONS_LIBRARY[current_course_key]
    lessons = course_data["videos"]

    # ---------------- HEADER ----------------
    section_header(
        f"🎥 {course_data['course_name']} Lessons",
        "Watch tutorial videos to learn step-by-step",
    )

    # Quick toggle to switch courses manually right on the lessons page
    all_courses = {k: v["course_name"] for k, v in LESSONS_LIBRARY.items()}
    selected_course_key = st.selectbox(
        "Switch Course Track",
        options=list(all_courses.keys()),
        format_func=lambda x: all_courses[x],
        index=list(all_courses.keys()).index(current_course_key),
    )

    # Handle explicit course track switching inside this view
    if selected_course_key != current_course_key:
        st.session_state["current_course"] = selected_course_key
        st.session_state["page"] = "🎥 Lessons"  # Keeps custom navigation shell aligned
        st.rerun()

    st.divider()

    # ---------------- FILTERS ----------------
    levels = ["All"] + sorted({lesson["level"] for lesson in lessons})
    selected_level = st.selectbox("Filter by difficulty level", levels)

    visible_lessons = lessons
    if selected_level != "All":
        visible_lessons = [
            l for l in lessons if l["level"] == selected_level
        ]

    st.caption(
        f"Showing {len(visible_lessons)} of {len(lessons)} tutorials in this track"
    )

    # ---------------- VIDEO CARDS ----------------
    for lesson in visible_lessons:
        with st.container(border=True):
            st.markdown(f"### {lesson['title']}")
            st.caption(f"📊 Level: {lesson['level']}")
            st.write(lesson["description"])
            st.video(lesson["url"])