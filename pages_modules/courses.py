"""Professional Courses Page."""

import streamlit as st
from utils.data_loader import get_active_data
from utils.ui_helpers import section_header


# ---------------- CACHE ----------------
@st.cache_data(ttl=3600)
def load_cached_courses():
    """Fetches and caches course data."""
    return get_active_data()


# ---------------- PAGE ----------------
def render():

    # ---------- HEADER ----------
    section_header(
        "📚 Courses",
        "Browse all available courses",
    )

    # ---------- LOAD DATA ----------
    df = load_cached_courses()

    if df is None or df.empty:
        st.warning("No course data available.")
        return

    st.divider()

    # ---------- FILTERS ----------
    f1, f2, f3 = st.columns([2, 1, 1])

    search = f1.text_input(
        "🔍 Search Courses",
        placeholder="e.g. Python",
    )

    categories = ["All"] + sorted(
        df["category"].dropna().unique().tolist()
    )

    category = f2.selectbox(
        "Category",
        categories,
    )

    sort_by = f3.selectbox(
        "Sort by",
        [
            "Most popular",
            "Highest rated",
            "Price (low to high)",
        ],
    )

    # ---------- FILTER LOGIC ----------
    filtered = df.copy()

    # Search
    if search:
        filtered = filtered[
            filtered["title"].str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    # Category
    if category != "All":
        filtered = filtered[
            filtered["category"] == category
        ]

    # Sorting
    if sort_by == "Most popular":
        filtered = filtered.sort_values(
            "enrolled_students",
            ascending=False,
        )

    elif sort_by == "Highest rated":
        filtered = filtered.sort_values(
            "rating",
            ascending=False,
        )

    else:
        filtered = filtered.sort_values(
            "price",
            ascending=True,
        )

    # ---------- RESULTS ----------
    st.caption(
        f"Showing {len(filtered)} of {len(df)} courses"
    )

    if filtered.empty:
        st.warning("No courses found.")
        return

    st.divider()

    # ---------- COURSE CARDS ----------
    rows = filtered.to_dict("records")

    for i in range(0, len(rows), 2):

        col1, col2 = st.columns(2)

        # ==========================================
        # LEFT CARD
        # ==========================================
        with col1:

            with st.container(border=True):

                course = rows[i]

                st.subheader(course["title"])
                st.caption(f"📂 {course['category']}")

                st.write(
                    f"👨‍🏫 Instructor: {course['instructor']}"
                )
                st.write(
                    f"⭐ Rating: {course['rating']}"
                )
                st.write(
                    f"👨‍🎓 Students: {course['enrolled_students']}"
                )
                st.write(
                    f"💰 Price: ${course['price']}"
                )

                completion = int(
                    course["completion_rate"]
                )

                st.progress(completion / 100)
                st.caption(
                    f"{completion}% completed"
                )

                # Course key for lessons routing
                course_key = course.get(
                    "course_key",
                    course.get("id", i),
                )

                if st.button(
                    "▶ Continue Learning",
                    key=f"left_{course_key}",
                    use_container_width=True,
                ):
                    st.toast(
                        f"{course['title']} Loaded 🚀"
                    )

                    # Store selected course
                    st.session_state[
                        "selected_course"
                    ] = course_key

                    # Navigate
                    st.session_state[
                        "go_to"
                    ] = "🎥 Lessons"

                    st.rerun()

        # ==========================================
        # RIGHT CARD
        # ==========================================
        if i + 1 < len(rows):

            with col2:

                with st.container(border=True):

                    course = rows[i + 1]

                    st.subheader(course["title"])
                    st.caption(
                        f"📂 {course['category']}"
                    )

                    st.write(
                        f"👨‍🏫 Instructor: {course['instructor']}"
                    )
                    st.write(
                        f"⭐ Rating: {course['rating']}"
                    )
                    st.write(
                        f"👨‍🎓 Students: {course['enrolled_students']}"
                    )
                    st.write(
                        f"💰 Price: ${course['price']}"
                    )

                    completion = int(
                        course["completion_rate"]
                    )

                    st.progress(
                        completion / 100
                    )
                    st.caption(
                        f"{completion}% completed"
                    )

                    # Course key
                    course_key = course.get(
                        "course_key",
                        course.get("id", i + 1),
                    )

                    if st.button(
                        "▶ Continue Learning",
                        key=f"right_{course_key}",
                        use_container_width=True,
                    ):
                        st.toast(
                            f"{course['title']} Loaded 🚀"
                        )

                        # Store selected course
                        st.session_state[
                            "selected_course"
                        ] = course_key

                        # Navigate
                        st.session_state[
                            "go_to"
                        ] = "🎥 Lessons"

                        st.rerun()