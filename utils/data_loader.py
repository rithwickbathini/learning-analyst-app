"""Loads course data from CSV (uploaded or sample)."""
import pandas as pd
import streamlit as st
from pathlib import Path

SAMPLE_PATH = Path(__file__).parent.parent / "data" / "sample_courses.csv"


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    """Load the bundled sample courses CSV."""
    return pd.read_csv(SAMPLE_PATH)


def get_active_data() -> pd.DataFrame:
    """Return uploaded data if user uploaded one, else sample data."""
    if "uploaded_df" in st.session_state and st.session_state.uploaded_df is not None:
        return st.session_state.uploaded_df
    return load_sample_data()