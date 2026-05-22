"""Session state management."""

import streamlit as st


def init_session():

    defaults = {
        "logged_in": False,
        "user_email": None,
        "user_role": "user",
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def login_user(email, role="user"):

    st.session_state.logged_in = True
    st.session_state.user_email = email
    st.session_state.user_role = role


def logout_user():

    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_role = "user"