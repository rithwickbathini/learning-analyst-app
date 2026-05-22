"""CSV uploader so users can replace sample data with their own."""

import pandas as pd
import streamlit as st

from utils.ui_helpers import section_header

REQUIRED = {
    "course_id",
    "title",
    "category",
    "instructor",
    "price",
    "enrolled_students",
    "rating",
    "duration_hours",
    "completion_rate",
}


def render():

    section_header(
        "📤 Upload Data",
        "Replace sample data with your own CSV"
    )

    st.markdown(
        "**Required columns:** "
        + ", ".join(f"`{c}`" for c in sorted(REQUIRED))
    )

    uploaded = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    # ---------------- FILE UPLOAD ----------------
    if uploaded is not None:

        try:
            df = pd.read_csv(uploaded)

        except Exception as e:
            st.error(f"Could not read CSV: {e}")
            return

        # Validate columns
        missing = REQUIRED - set(df.columns)

        if missing:
            st.error(
                f"Missing required columns: "
                f"{', '.join(sorted(missing))}"
            )
            return

        # Save uploaded dataframe
        st.session_state.uploaded_df = df

        # Success message
        st.success(
            f"✅ Loaded {len(df)} courses! "
            f"All pages now use your data."
        )

        # Toast notification
        st.toast("Data uploaded successfully 📤")

        # Preview table
        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    # ---------------- REVERT BUTTON ----------------
    if (
        "uploaded_df" in st.session_state
        and st.session_state.uploaded_df is not None
    ):

        if st.button("↩️ Revert to sample data"):

            st.session_state.uploaded_df = None

            st.toast("Reverted to sample data 🔄")

            st.rerun()

            st.markdown("---")
            st.caption("© 2026 Learning Platform")