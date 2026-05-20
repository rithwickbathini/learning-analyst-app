"""Reusable UI components: KPI tiles, course cards, section headers."""
import streamlit as st


def section_header(title: str, subtitle: str = ""):
    """Standardized header used at the top of every page."""
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()


def course_card(row):
    """Render a single course as a styled card."""
    with st.container(border=True):
        st.markdown(f"### {row['title']}")
        st.caption(f"📚 {row['category']}  •  👤 {row['instructor']}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Price", f"${row['price']:.2f}")
        c2.metric("Rating", f"⭐ {row['rating']}")
        c3.metric("Students", f"{int(row['enrolled_students']):,}")

        st.progress(
            int(row["completion_rate"]) / 100,
            text=f"Avg completion: {int(row['completion_rate'])}%",
        )