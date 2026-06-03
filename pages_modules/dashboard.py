"""Dashboard page: KPIs and analytics."""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import get_active_data
from utils.ui_helpers import section_header


# ---------------- CACHE ----------------
@st.cache_data(ttl=600)
def load_dashboard_data():
    """Load and cache dashboard data."""
    return get_active_data()


# ---------------- RENDER ----------------
def render():

    # ---------------- HEADER ----------------
    section_header(
        "📊 Analytics Dashboard",
        "Overview of learning performance and platform growth",
    )

    st.divider()

    # ---------------- LOAD DATA ----------------
    df = load_dashboard_data()

    # ---------------- SAFETY CHECK ----------------
    if df is None or df.empty:
        st.warning("No data available to display.")
        return

    # ---------------- KPI CALCULATIONS ----------------
    total_students = int(
        df["enrolled_students"].sum()
    )

    total_revenue = (
        df["enrolled_students"] * df["price"]
    ).sum()

    avg_rating = df["rating"].mean()

    avg_completion = df["completion_rate"].mean()

    # ---------------- TOP METRICS ----------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Enrollments",
            f"{total_students:,}",
            "+12%"
        )

    with c2:
        st.metric(
            "Revenue",
            f"${total_revenue:,.0f}",
            "+18%"
        )

    with c3:
        st.metric(
            "Avg Rating",
            f"⭐ {avg_rating:.2f}",
            "+0.3"
        )

    with c4:
        st.metric(
            "Completion",
            f"{avg_completion:.1f}%",
            "+6%"
        )

    st.divider()

    # ---------------- QUICK USER STATS ----------------
    st.subheader("📈 Student Learning Performance")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Courses Completed",
            "18",
            "+3"
        )

    with c2:
        st.metric(
            "Quiz Average",
            "87%",
            "+5%"
        )

    with c3:
        st.metric(
            "Certificates",
            "6",
            "+1"
        )

    st.divider()

    # ---------------- INTERACTIVE LINE CHART ----------------
    st.subheader("📅 Learning Growth Trends")

    analytics_df = pd.DataFrame({
        "Month": [
            "Jan", "Feb", "Mar",
            "Apr", "May", "Jun"
        ] * 3,

        "Track":
            ["ServiceNow"] * 6 +
            ["Python"] * 6 +
            ["AI"] * 6,

        "Score": [
            60, 65, 70, 74, 80, 88,
            50, 58, 64, 70, 76, 82,
            62, 68, 72, 79, 84, 91
        ]
    })

    fig1 = px.line(
        analytics_df,
        x="Month",
        y="Score",
        color="Track",
        markers=True,
        line_shape="spline",
        hover_data=["Track", "Score"],
        title="Learning Performance Trends"
    )

    fig1.update_traces(
        line=dict(width=4),
        marker=dict(size=10)
    )

    fig1.update_layout(
        transition_duration=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=450,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.divider()

    # ---------------- WEEKLY ACTIVITY ----------------
    st.subheader("⏱ Weekly Study Activity")

    activity_df = pd.DataFrame({
        "Day": [
            "Mon", "Tue", "Wed",
            "Thu", "Fri", "Sat", "Sun"
        ],
        "Hours": [2, 3, 1, 4, 5, 6, 3]
    })

    fig2 = px.area(
        activity_df,
        x="Day",
        y="Hours",
        markers=True,
        title="Weekly Learning Hours"
    )

    fig2.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=400
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.divider()

    # ---------------- ANALYTICS CHARTS ----------------
    col1, col2 = st.columns(2)

    # ---------------- BAR CHART ----------------
    with col1:

        st.subheader("📚 Enrollments by Category")

        cat_df = (
            df.groupby(
                "category",
                as_index=False
            )["enrolled_students"]
            .sum()
        )

        fig3 = px.bar(
            cat_df,
            x="category",
            y="enrolled_students",
            text="enrolled_students",
            color="category",
            title="Course Popularity"
        )

        fig3.update_traces(
            textposition="outside"
        )

        fig3.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # ---------------- PIE / DONUT CHART ----------------
    with col2:

        st.subheader("💰 Revenue Distribution")

        rev_df = df.copy()

        rev_df["revenue"] = (
            rev_df["enrolled_students"] *
            rev_df["price"]
        )

        rev_cat = rev_df.groupby(
            "category",
            as_index=False
        )["revenue"].sum()

        fig4 = px.pie(
            rev_cat,
            names="category",
            values="revenue",
            hole=0.45,
            title="Revenue Share"
        )

        fig4.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.divider()

    # ---------------- TOP COURSES ----------------
    st.subheader("🏆 Top Performing Courses")

    top_courses = df.nlargest(
        5,
        "enrolled_students"
    )[
        [
            "title",
            "category",
            "instructor",
            "enrolled_students",
            "rating"
        ]
    ]

    st.dataframe(
        top_courses,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ---------------- AI INSIGHTS ----------------
    st.subheader("🤖 AI Insights")

    st.success(
        """
✔ ServiceNow courses show highest completion rates.

✔ AI track engagement increased by 24%.

✔ Students who complete quizzes weekly perform 31% better.

✔ Weekend learning activity is growing rapidly.
        """
    )

    # ---------------- TOAST ----------------
    st.toast(
        "Dashboard Analytics Loaded 🚀"
    )