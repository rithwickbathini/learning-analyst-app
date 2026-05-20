"""Database connection to Supabase (PostgreSQL)."""
import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


@st.cache_resource
def get_db():
    """Create and cache a single Supabase client for the whole app."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    # On Streamlit Cloud, secrets come from st.secrets instead of .env
    if not url and hasattr(st, "secrets"):
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")

    if not url or not key:
        return None

    from supabase import create_client
    return create_client(url, key)