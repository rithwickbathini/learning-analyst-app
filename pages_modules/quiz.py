"""90-day quiz engine. Reads questions from quiz_data.py."""

import streamlit as st
from pages_modules.quiz_data import QUIZ_DATA
from utils.ui_helpers import section_header

# Import DB + auth, but degrade gracefully if not set up
try:
    from utils.db import get_db
    from utils.auth import current_email

    _DB_AVAILABLE = True
except Exception:
    _DB_AVAILABLE = False


def render():
    section_header("📝 90-Day Quiz Challenge", "10 questions a day, basic to expert")

    total_days = 90
    available_days = sorted(QUIZ_DATA.keys())

    st.caption(
        f"{len(available_days)} of {total_days} days available so far. More added regularly."
    )

    # Initialize session state tracking keys for this day's submission
    day_picker_key = "current_quiz_day"
    if day_picker_key not in st.session_state:
        st.session_state[day_picker_key] = 1

    # Day picker — show all 90, mark which are ready
    day = st.selectbox(
        "Choose a day",
        range(1, total_days + 1),
        format_func=lambda d: f"Day {d}"
        + ("" if d in QUIZ_DATA else " — coming soon"),
        key=day_picker_key,
    )

    if day not in QUIZ_DATA:
        st.info(f"Day {day} hasn't been added yet. Pick a day marked as available.")
        return

    quiz = QUIZ_DATA[day]
    questions = quiz["questions"]
    st.markdown(f"#### Day {day}: {quiz['topic']}")
    st.caption(f"{len(questions)} questions • Pass mark: 70%")
    st.divider()

    # Create dynamic keys for this specific day's submission tracking
    submit_state_key = f"submitted_day_{day}"
    answers_state_key = f"answers_day_{day}"

    # Render questions
    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i + 1}. {q['q']}**")

        # Disable the radio inputs once they've submitted so they can lock in answers
        is_disabled = st.session_state.get(submit_state_key, False)

        choice = st.radio(
            "Select your answer",
            options=list(range(len(q["options"]))),
            format_func=lambda idx, opts=q["options"]: opts[idx],
            key=f"day{day}_q{i}",
            index=None,
            label_visibility="collapsed",
            disabled=is_disabled,
        )
        user_answers.append(choice)
        st.markdown("")

    # --- SUBMIT HANDLING ---
    if not st.session_state.get(submit_state_key, False):
        if st.button("Submit Quiz", type="primary"):
            if None in user_answers:
                st.warning("Please answer all questions before submitting.")
                return

            # Score logic
            score = sum(
                1
                for i, q in enumerate(questions)
                if user_answers[i] == q["correct"]
            )
            total = len(questions)
            percentage = round(score / total * 100)

            # Save metrics to session state so they persist across reruns
            st.session_state[submit_state_key] = True
            st.session_state[answers_state_key] = {
                "score": score,
                "total": total,
                "percentage": percentage,
                "saved_answers": user_answers,
            }

            # Save to database if available
            if _DB_AVAILABLE:
                db = get_db()
                if db is not None:
                    try:
                        db.table("quiz_scores").insert(
                            {
                                "user_email": current_email(),
                                "quiz_name": f"Day {day}: {quiz['topic']}",
                                "score": score,
                                "total": total,
                                "percentage": percentage,
                            }
                        ).execute()
                    except Exception:
                        pass  # Fail gracefully if DB write hiccups

            st.rerun()

    # --- PERSISTENT RESULTS DISPLAY ---
    if st.session_state.get(submit_state_key, False):
        results = st.session_state[answers_state_key]
        score = results["score"]
        total = results["total"]
        percentage = results["percentage"]
        saved_answers = results["saved_answers"]

        st.divider()
        st.markdown("### Results")
        c1, c2 = st.columns(2)
        c1.metric("Score", f"{score} / {total}")
        c2.metric("Percentage", f"{percentage}%")

        if percentage >= 70:
            st.success(f"🎉 Passed! You scored {percentage}%.")
        else:
            st.error(
                f"You scored {percentage}%. Review and try again to reach 70."
            )

        st.markdown("#### Review")
        for i, q in enumerate(questions):
            correct_text = q["options"][q["correct"]]
            chosen_text = q["options"][saved_answers[i]]
            if saved_answers[i] == q["correct"]:
                st.markdown(f"✅ **Q{i + 1}**: {chosen_text}")
            else:
                st.markdown(
                    f"❌ **Q{i + 1}**: You chose *{chosen_text}* — correct: **{correct_text}**"
                )

        # Allow them to retry and clear state
        st.write("")
        if st.button("🔄 Clear Results & Retry"):
            del st.session_state[submit_state_key]
            del st.session_state[answers_state_key]
            # Clear individual radio widget states too
            for i in range(len(questions)):
                if f"day{day}_q{i}" in st.session_state:
                    del st.session_state[f"day{day}_q{i}"]
            st.rerun()