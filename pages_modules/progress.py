"""Student progress section."""
import plotly.express as px
import streamlit as st

from utils.data_loader import get_active_data
from utils.ui_helpers import section_header


def render():
    section_header("🎯 My Progress", "Track learning across enrolled courses")
    df = get_active_data().copy()

    my = df.head(5).copy()
    my["my_progress"] = (my["completion_rate"] * 0.9).astype(int).clip(5, 100)

    c1, c2, c3 = st.columns(3)
    c1.metric("Courses Enrolled", len(my))
    c2.metric("Avg Progress", f"{my['my_progress'].mean():.0f}%")
    c3.metric("Completed", int((my["my_progress"] >= 100).sum()))

    st.markdown("#### Course Progress")
    for _, row in my.iterrows():
        with st.container(border=True):
            top = st.columns([3, 1])
            top[0].markdown(f"**{row['title']}**  \n*{row['instructor']} • {row['category']}*")
            top[1].metric("Progress", f"{row['my_progress']}%")
            st.progress(row["my_progress"] / 100)

    st.markdown("#### Progress Overview")
    fig = px.bar(my, x="my_progress", y="title", orientation="h",
                 color="my_progress", color_continuous_scale="Blues", text="my_progress")
    fig.update_layout(yaxis_title="", xaxis_title="Progress (%)", height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.caption("© 2026 Learning Platform")