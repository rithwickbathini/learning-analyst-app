"""Quiz page: multiple-choice Python quizzes with scoring."""
import streamlit as st

from utils.ui_helpers import section_header

# Quiz bank. Each quiz has a title and a list of questions.
# Each question: the prompt, the options, and the index of the correct option.
QUIZZES = {
    "Python Basics": [
        {
            "question": "Which keyword defines a function in Python?",
            "options": ["func", "def", "function", "define"],
            "correct": 1,
        },
        {
            "question": "What data type is the result of: 3 / 2 ?",
            "options": ["int", "float", "string", "bool"],
            "correct": 1,
        },
        {
            "question": "How do you start a comment in Python?",
            "options": ["//", "<!--", "#", "/*"],
            "correct": 2,
        },
        {
            "question": "Which of these is a valid list?",
            "options": ["{1, 2, 3}", "(1, 2, 3)", "[1, 2, 3]", "<1, 2, 3>"],
            "correct": 2,
        },
    ],
    "Data Structures": [
        {
            "question": "Which structure stores key-value pairs?",
            "options": ["list", "tuple", "set", "dictionary"],
            "correct": 3,
        },
        {
            "question": "Which structure does NOT allow duplicate values?",
            "options": ["list", "set", "tuple", "string"],
            "correct": 1,
        },
        {
            "question": "Tuples in Python are:",
            "options": ["mutable", "immutable", "always empty", "key-value pairs"],
            "correct": 1,
        },
    ],
}


def render():
    section_header("📝 Quizzes", "Test your knowledge")

    # Pick a quiz
    quiz_name = st.selectbox("Choose a quiz", list(QUIZZES.keys()))
    questions = QUIZZES[quiz_name]

    st.caption(f"{len(questions)} questions • Choose one answer each")
    st.divider()

    # Collect answers. We use a unique key per question so Streamlit tracks them.
    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i + 1}. {q['question']}**")
        choice = st.radio(
            "Select your answer",
            options=list(range(len(q["options"]))),
            format_func=lambda idx, opts=q["options"]: opts[idx],
            key=f"{quiz_name}_q{i}",
            index=None,  # no pre-selected answer
            label_visibility="collapsed",
        )
        user_answers.append(choice)
        st.markdown("")

    # Submit and score
    if st.button("Submit Quiz", type="primary"):
        if None in user_answers:
            st.warning("Please answer all questions before submitting.")
            return

        score = sum(
            1 for i, q in enumerate(questions) if user_answers[i] == q["correct"]
        )
        total = len(questions)
        percentage = round(score / total * 100)

        st.divider()
        st.markdown("### Results")
        c1, c2 = st.columns(2)
        c1.metric("Score", f"{score} / {total}")
        c2.metric("Percentage", f"{percentage}%")

        if percentage >= 70:
            st.success(f"🎉 Passed! You scored {percentage}%.")
            st.balloons()
        else:
            st.error(f"You scored {percentage}%. Try again to reach 70%.")

        # Show which answers were right/wrong
        st.markdown("#### Review")
        for i, q in enumerate(questions):
            correct_text = q["options"][q["correct"]]
            chosen_text = q["options"][user_answers[i]]
            if user_answers[i] == q["correct"]:
                st.markdown(f"✅ **Q{i + 1}**: {chosen_text}")
            else:
                st.markdown(
                    f"❌ **Q{i + 1}**: You chose *{chosen_text}* — correct answer: **{correct_text}**"
                )