"""Login and signup screen shown when the user is not logged in."""
import streamlit as st

from utils.auth import login_user, register_user


def render():
    st.title("🎓 Learning Platform")
    st.caption("Please log in or create an account to continue.")

    tab_login, tab_signup = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary"):
            ok, msg = login_user(email, password)
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
        st.caption("Demo admin → email: admin@app.com  •  password: admin123")

    with tab_signup:
        name = st.text_input("Full name", key="signup_name")
        new_email = st.text_input("Email", key="signup_email")
        new_pw = st.text_input("Password", type="password", key="signup_password")
        confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
        if st.button("Create account", type="primary"):
            if new_pw != confirm:
                st.error("Passwords do not match.")
            else:
                ok, msg = register_user(new_email, name, new_pw, role="student")
                st.success(msg) if ok else st.error(msg)