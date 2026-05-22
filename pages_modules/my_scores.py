"""Student score history: shows each user their own past quiz results."""
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.auth import current_email
from utils.db import get_db
from utils.ui_helpers import section_header


def render():
    section_header("📈 My Scores", "Your quiz history and progress over time")

    db = get_db()
    if db is None:
        st.error("Database not connected. Scores can't be loaded.")
        return

    email = current_email()

    # Fetch this user's scores, newest first
    result = (
        db.table("quiz_scores")
        .select("quiz_name, score, total, percentage, taken_at")
        .eq("user_email", email)
        .order("taken_at", desc=True)
        .execute()
    )
    rows = result.data

    if not rows:
        st.info("You haven't taken any quizzes yet. Head to 📝 Quizzes to start!")
        return

    df = pd.DataFrame(rows)

    # Summary KPIs
    total_quizzes = len(df)
    avg_score = df["percentage"].mean()
    best_score = df["percentage"].max()
    passed = int((df["percentage"] >= 70).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quizzes Taken", total_quizzes)
    c2.metric("Average", f"{avg_score:.0f}%")
    c3.metric("Best Score", f"{best_score}%")
    c4.metric("Passed", f"{passed}/{total_quizzes}")

    st.divider()

    # Progress-over-time chart (oldest to newest)
    st.markdown("#### Score Trend")
    chart_df = df.sort_values("taken_at").reset_index(drop=True)
    chart_df["attempt"] = range(1, len(chart_df) + 1)
    fig = px.line(
        chart_df,
        x="attempt",
        y="percentage",
        markers=True,
        labels={"attempt": "Attempt #", "percentage": "Score (%)"},
    )
    fig.add_hline(y=70, line_dash="dash", line_color="green",
                  annotation_text="Pass mark (70%)")
    fig.update_layout(height=350, yaxis_range=[0, 105])
    st.plotly_chart(fig, use_container_width=True)

    # Full history table
    st.markdown("#### Full History")
    display = df.copy()
    display["Result"] = display["percentage"].apply(lambda p: "✅ Pass" if p >= 70 else "❌ Fail")
    display = display.rename(columns={
        "quiz_name": "Quiz",
        "score": "Correct",
        "total": "Total",
        "percentage": "Score %",
        "taken_at": "Date",
    })
    # Tidy the date (keep just date + time, drop microseconds)
    display["Date"] = pd.to_datetime(display["Date"]).dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(
        display[["Quiz", "Correct", "Total", "Score %", "Result", "Date"]],
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("---")
    st.caption("© 2026 Learning Platform")