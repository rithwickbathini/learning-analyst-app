"""Lessons page: Python tutorial videos."""
import streamlit as st

from utils.ui_helpers import section_header

# Your video library. Add as many as you like.
# Just paste a normal YouTube URL into "url".
LESSONS = [
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
]


def render():
    section_header("🎥 Python Lessons", "Watch tutorial videos to learn Python")

    # Optional: filter by level
    levels = ["All"] + sorted({lesson["level"] for lesson in LESSONS})
    selected = st.selectbox("Filter by level", levels)

    visible = LESSONS
    if selected != "All":
        visible = [l for l in LESSONS if l["level"] == selected]

    st.caption(f"Showing {len(visible)} of {len(LESSONS)} lessons")

    for lesson in visible:
        with st.container(border=True):
            st.markdown(f"### {lesson['title']}")
            st.caption(f"📊 Level: {lesson['level']}")
            st.write(lesson["description"])
            st.video(lesson["url"])