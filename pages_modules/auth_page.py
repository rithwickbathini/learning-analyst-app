"""Login and signup screen shown when the user is not logged in."""

import streamlit as st
from utils.auth import login_user, register_user


def render():

    # ---------------- CUSTOM CSS ----------------
    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
    }

    .auth-card {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-top: 60px;
    }

    .stTextInput input {
        border-radius: 10px;
    }

    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-size: 16px;
        font-weight: 600;
        background-color: #2563eb;
        color: white;
        border: none;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------- CENTERED LAYOUT ----------------
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        st.markdown(
            """
            <div style='text-align: center;'>
                <img src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
                     width='100'>
                <h2>🎓 Learning Platform</h2>
                <p style="color: gray;">AI Powered Learning System</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

        # LOGIN
        with tab_login:

            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", type="primary"):

                with st.spinner("Logging in..."):
                    ok, msg = login_user(email, password)

                if ok:
                    st.toast("Login successful ✅")
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        # SIGNUP
        with tab_signup:

            name = st.text_input("Full Name", key="signup_name")
            new_email = st.text_input("Email", key="signup_email")
            new_pw = st.text_input("Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

            if st.button("Create Account", type="primary"):

                if new_pw != confirm:
                    st.error("Passwords do not match.")
                else:
                    with st.spinner("Creating account..."):
                        ok, msg = register_user(new_email, name, new_pw, role="student")

                    if ok:
                        st.toast("Account created 🎉")
                        st.success(msg)
                    else:
                        st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2026 Learning Platform")