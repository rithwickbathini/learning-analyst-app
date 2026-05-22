"""Database connection utilities."""

import streamlit as st
from config.settings import SUPABASE_KEY, SUPABASE_URL


@st.cache_resource
def get_db():
    """Initializes and caches the Supabase client connection."""
    if not SUPABASE_URL:
        st.error("Missing SUPABASE_URL")
        return None

    if not SUPABASE_KEY:
        st.error("Missing SUPABASE_KEY")
        return None

    try:
        from supabase import create_client

        return create_client(SUPABASE_URL, SUPABASE_KEY)

    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None