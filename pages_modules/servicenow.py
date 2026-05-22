"""ServiceNow learning track: real YouTube classes, basic to expert."""
import streamlit as st

from utils.ui_helpers import section_header

# Real ServiceNow tutorial videos, grouped by level.
# To add more: copy a YouTube URL into a new entry under the right level.
SERVICENOW_CLASSES = {
    "Beginner": [
        {"title": "ServiceNow Tutorial for Beginners — Full Course",
         "description": "Complete beginner course covering ITSM basics to core platform features.",
         "url": "https://www.youtube.com/watch?v=pqKc74DumAI"},
        {"title": "ServiceNow Admin — Part 1 (Learn Administration)",
         "description": "Step-by-step beginner's guide to mastering ServiceNow administration.",
         "url": "https://www.youtube.com/watch?v=7f4BYhxzNG0"},
        {"title": "Master ServiceNow — Beginner to Expert (2025)",
         "description": "Beginner-friendly full course covering the platform end to end.",
         "url": "https://www.youtube.com/watch?v=7iqqgZ_FvSw"},
    ],
    "Intermediate": [
        {"title": "ServiceNow Developer Full Course — Client Scripts",
         "description": "Core developer skills: client scripts and platform configuration.",
         "url": "https://www.youtube.com/watch?v=WLNQinTkLfQ"},
        {"title": "ServiceNow Scripting 101 — Intro to GlideRecord",
         "description": "Server-side scripting basics: query, update, and insert records.",
         "url": "https://www.youtube.com/watch?v=SJlSEom0UvI"},
    ],
    "Advanced / Expert": [
        {"title": "ServiceNow Scripting — GlideRecord Methods (Practical)",
         "description": "Advanced practical demo of GlideRecord and reusable utilities.",
         "url": "https://www.youtube.com/watch?v=gAO5l6MQC2E"},
        {"title": "GlideRecord — Scripting & Demo (Deep Dive)",
         "description": "In-depth GlideRecord scripting with real-world examples.",
         "url": "https://www.youtube.com/watch?v=Cx3p2SxyEPg"},
    ],
}


def render():
    section_header("🧩 ServiceNow Classes", "Learn ServiceNow from basic to expert")

    levels = list(SERVICENOW_CLASSES.keys())
    selected = st.radio("Choose your level", levels, horizontal=True)

    classes = SERVICENOW_CLASSES[selected]
    st.caption(f"{len(classes)} classes in **{selected}**")
    st.divider()

    for cls in classes:
        with st.container(border=True):
            st.markdown(f"### {cls['title']}")
            st.write(cls["description"])
            st.video(cls["url"])