"""Courses page: searchable, filterable grid of course cards."""
import streamlit as st

from utils.data_loader import get_active_data
from utils.ui_helpers import course_card, section_header


def render():
    section_header("📚 Courses", "Browse all available courses")
    df = get_active_data()

    f1, f2, f3 = st.columns([2, 1, 1])
    search = f1.text_input("🔍 Search", placeholder="e.g. Python")
    cats = ["All"] + sorted(df["category"].unique().tolist())
    category = f2.selectbox("Category", cats)
    sort_by = f3.selectbox("Sort by", ["Most popular", "Highest rated", "Price (low to high)"])

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["title"].str.contains(search, case=False, na=False)]
    if category != "All":
        filtered = filtered[filtered["category"] == category]

    if sort_by == "Most popular":
        filtered = filtered.sort_values("enrolled_students", ascending=False)
    elif sort_by == "Highest rated":
        filtered = filtered.sort_values("rating", ascending=False)
    else:
        filtered = filtered.sort_values("price", ascending=True)

    st.caption(f"Showing {len(filtered)} of {len(df)} courses")
    if filtered.empty:
        st.info("No courses match your filters.")
        return

    rows = filtered.to_dict("records")
    for i in range(0, len(rows), 2):
        col_l, col_r = st.columns(2)
        with col_l:
            course_card(rows[i])
        if i + 1 < len(rows):
            with col_r:
                course_card(rows[i + 1])