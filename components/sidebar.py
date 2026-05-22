"""Professional Sidebar Navigation."""

import streamlit as st


def render_sidebar(role):

    with st.sidebar:

        # Profile Image
        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=90,
        )

        # App Title
        st.title("🎓 Learning Platform")
        st.caption("AI Powered Learning")

        st.divider()

        # User Info
        st.write("👋 Welcome")

        st.caption(
            st.session_state.get("user_name", "User")
        )

        st.write(
            f"📧 {st.session_state.get('user_email', 'No Email')}"
        )

        st.write(
            f"🛡️ Role: {role.capitalize()}"
        )

        st.divider()

        # Menu Options
        if role == "admin":

            options = [
                "🏠 Home",
                "📊 Dashboard",
                "📚 Courses",
                "🎥 Lessons",
                "📝 Quizzes",
                "📈 My Scores",
                "🎯 Progress",
                "📤 Upload Data",
                "🛠️ Admin Panel",
            ]

        else:

            options = [
                "🏠 Home",
                "📊 Dashboard",
                "📚 Courses",
                "🎥 Lessons",
                "📝 Quizzes",
                "📈 My Scores",
                "🎯 Progress",
            ]

        # Navigation
        page = st.radio(
            "Navigation",
            options,
            label_visibility="collapsed",
        )

        st.divider()

        # Logout Button
        if st.button(
            "🚪 Logout",
            use_container_width=True,
        ):
            from utils.auth import logout_user

            logout_user()
            st.rerun()

    return page