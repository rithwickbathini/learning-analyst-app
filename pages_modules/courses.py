"""Professional Courses Page."""

import time
import streamlit as st

from utils.data_loader import get_active_data
from utils.ui_helpers import section_header


def render():

    # ---------------- HEADER ----------------
    section_header(
        "📚 Courses",
        "Browse all available courses",
    )

    # ---------------- LOADING ----------------
    with st.spinner("Loading courses..."):
        time.sleep(1.5)
        df = get_active_data()

    st.success("Courses loaded successfully")

    st.divider()

    # ---------------- FILTERS ----------------
    f1, f2, f3 = st.columns([2, 1, 1])

    search = f1.text_input(
        "🔍 Search Courses",
        placeholder="e.g. Python",
    )

    categories = ["All"] + sorted(
        df["category"].unique().tolist()
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

    # ---------------- FILTER LOGIC ----------------
    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["title"].str.contains(
                search,
                case=False,
                na=False,
            )
        ]

    if category != "All":
        filtered = filtered[
            filtered["category"] == category
        ]

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

    # ---------------- RESULTS ----------------
    st.caption(
        f"Showing {len(filtered)} of {len(df)} courses"
    )

    if filtered.empty:
        st.warning("No courses found.")
        return

    st.divider()

    # ---------------- COURSE CARDS ----------------
    rows = filtered.to_dict("records")

    for i in range(0, len(rows), 2):

        col1, col2 = st.columns(2)

        # ---------- LEFT CARD ----------
        with col1:

            with st.container(border=True):

                st.subheader(rows[i]["title"])

                st.caption(
                    f"📂 {rows[i]['category']}"
                )

                st.write(
                    f"👨‍🏫 Instructor: "
                    f"{rows[i]['instructor']}"
                )

                st.write(
                    f"⭐ Rating: "
                    f"{rows[i]['rating']}"
                )

                st.write(
                    f"👨‍🎓 Students: "
                    f"{rows[i]['enrolled_students']}"
                )

                st.write(
                    f"💰 Price: "
                    f"${rows[i]['price']}"
                )

                completion = int(
                    rows[i]["completion_rate"]
                )

                st.progress(completion / 100)

                st.caption(
                    f"{completion}% completed"
                )

                st.button(
                    "▶ Continue Learning",
                    key=f"left_{i}",
                    use_container_width=True,
                )

        # ---------- RIGHT CARD ----------
        if i + 1 < len(rows):

            with col2:

                with st.container(border=True):

                    st.subheader(rows[i + 1]["title"])

                    st.caption(
                        f"📂 {rows[i + 1]['category']}"
                    )

                    st.write(
                        f"👨‍🏫 Instructor: "
                        f"{rows[i + 1]['instructor']}"
                    )

                    st.write(
                        f"⭐ Rating: "
                        f"{rows[i + 1]['rating']}"
                    )

                    st.write(
                        f"👨‍🎓 Students: "
                        f"{rows[i + 1]['enrolled_students']}"
                    )

                    st.write(
                        f"💰 Price: "
                        f"${rows[i + 1]['price']}"
                    )

                    completion = int(
                        rows[i + 1]["completion_rate"]
                    )

                    st.progress(completion / 100)

                    st.caption(
                        f"{completion}% completed"
                    )

                    st.button(
                        "▶ Continue Learning",
                        key=f"right_{i}",
                        use_container_width=True,
                    )
                    st.markdown("---")
                    st.caption("© 2026 Learning Platform")