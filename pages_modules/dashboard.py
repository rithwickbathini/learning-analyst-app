"""Dashboard page: KPIs and analytics."""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import get_active_data
from utils.ui_helpers import section_header


def render():

    # ---------------- HEADER ----------------
    section_header(
        "📊 Dashboard",
        "Overview of platform performance",
    )

    # ---------------- LOAD DATA ----------------
    with st.spinner("Loading dashboard..."):
        df = get_active_data()

    # ---------------- SAFETY CHECK ----------------
    if df is None or df.empty:
        st.warning("No data available to display.")
        return

    # ---------------- KPI CALCULATIONS ----------------
    total_students = int(df["enrolled_students"].sum())

    total_revenue = (
        df["enrolled_students"] * df["price"]
    ).sum()

    avg_rating = df["rating"].mean()
    avg_completion = df["completion_rate"].mean()

    # ---------------- TOP METRICS ----------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Enrollments", f"{total_students:,}")

    with c2:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")

    with c3:
        st.metric("Avg Rating", f"⭐ {avg_rating:.2f}")

    with c4:
        st.metric("Avg Completion", f"{avg_completion:.1f}%")

    st.divider()

    # ---------------- QUICK USER STATS ----------------
    st.subheader("📈 Learning Performance")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Courses", 12, "+2")

    with c2:
        st.metric("Completed", 8, "+1")

    with c3:
        st.metric("Quiz Average", "87%", "+5%")

    st.divider()

    # ---------------- WEEKLY ACTIVITY LINE CHART ----------------
    st.subheader("📅 Weekly Study Activity")

    activity_df = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Hours": [2, 3, 1, 4, 5],
    })

    fig1 = px.line(
        activity_df,
        x="Day",
        y="Hours",
        markers=True,
        title="Study Hours Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ---------------- ANALYTICS CHARTS ----------------
    col1, col2 = st.columns(2)

    # ---------- BAR CHART ----------
    with col1:

        st.subheader("📚 Enrollments by Category")

        cat_df = df.groupby(
            "category",
            as_index=False
        )["enrolled_students"].sum()

        fig2 = px.bar(
            cat_df,
            x="category",
            y="enrolled_students",
            text="enrolled_students",
        )

        fig2.update_layout(
            height=350,
            showlegend=False,
            xaxis_title="Category",
            yaxis_title="Enrollments",
        )

        st.plotly_chart(fig2, use_container_width=True)

    # ---------- PIE CHART ----------
    with col2:

        st.subheader("💰 Revenue Distribution")

        rev_df = df.copy()
        rev_df["revenue"] = rev_df["enrolled_students"] * rev_df["price"]

        rev_cat = rev_df.groupby(
            "category",
            as_index=False
        )["revenue"].sum()

        fig3 = px.pie(
            rev_cat,
            names="category",
            values="revenue",
            hole=0.4,
        )

        fig3.update_layout(height=350)

        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ---------------- TOP COURSES TABLE ----------------
    st.subheader("🏆 Top Performing Courses")

    top_courses = df.nlargest(5, "enrolled_students")[
        ["title", "category", "instructor", "enrolled_students", "rating"]
    ]

    st.dataframe(
        top_courses,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.caption("© 2026 Learning Platform")