"""AI Tutor page: chat-style learning assistant."""

import streamlit as st


def render():

    # ---------------- PAGE TITLE ----------------
    st.title("🤖 AI Tutor")
    st.caption("Ask anything and learn interactively")

    # ---------------- SESSION MEMORY ----------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------------- DISPLAY CHAT HISTORY ----------------
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

    # ---------------- USER INPUT ----------------
    prompt = st.chat_input("Ask AI anything...")

    if prompt:

        # Show user message
        st.chat_message("user").write(prompt)

        # Fake AI response (replace later with real API)
        response = f"🤖 I understand your question: '{prompt}'. Let me explain step by step..."

        # Store in memory
        st.session_state.chat_history.append(("user", prompt))
        st.session_state.chat_history.append(("assistant", response))

        # Show assistant response
        with st.chat_message("assistant"):
            st.write(response)