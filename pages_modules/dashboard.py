"""Dashboard page: KPIs and charts."""
import plotly.express as px
import streamlit as st

from utils.data_loader import get_active_data
from utils.ui_helpers import section_header


def render():
    section_header("📊 Dashboard", "Overview of platform performance")
    df = get_active_data()

    total_students = int(df["enrolled_students"].sum())
    total_revenue = (df["enrolled_students"] * df["price"]).sum()
    avg_rating = df["rating"].mean()
    avg_completion = df["completion_rate"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Enrollments", f"{total_students:,}")
    c2.metric("Total Revenue", f"${total_revenue:,.0f}")
    c3.metric("Avg Rating", f"⭐ {avg_rating:.2f}")
    c4.metric("Avg Completion", f"{avg_completion:.1f}%")

    st.markdown("")
    left, right = st.columns(2)

    with left:
        st.markdown("#### Enrollments by Category")
        cat = df.groupby("category", as_index=False)["enrolled_students"].sum()
        fig = px.bar(cat, x="category", y="enrolled_students", color="category", text="enrolled_students")
        fig.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig, width='stretch')

    with right:
        st.markdown("#### Revenue Share by Category")
        rev = df.copy()
        rev["revenue"] = rev["enrolled_students"] * rev["price"]
        rev_cat = rev.groupby("category", as_index=False)["revenue"].sum()
        fig = px.pie(rev_cat, names="category", values="revenue", hole=0.45)
        fig.update_layout(height=350)
        st.plotly_chart(fig, width='stretch')

    st.markdown("#### Top Courses by Enrollment")
    top = df.nlargest(5, "enrolled_students")[["title", "category", "instructor", "enrolled_students", "rating"]]
    st.dataframe(top, width='stretch', hide_index=True)