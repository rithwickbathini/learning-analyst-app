"""Database connection to Supabase (PostgreSQL)."""
import os

import streamlit as st


@st.cache_resource
def get_db():
    url = None
    key = None

    # 1) Streamlit Cloud secrets
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        pass

    # 2) Local .env fallback
    if not url or not key:
        try:
            from dotenv import load_dotenv

            load_dotenv()

            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

        except Exception:
            pass

    # DEBUG BLOCK
    if not url or not key:
        try:
            available = list(st.secrets.keys())
        except Exception as e:
            available = f"st.secrets error: {e}"

        st.warning(
            f"DEBUG → url found: {bool(url)} | "
            f"key found: {bool(key)} | "
            f"secrets seen: {available}"
        )

        return None

    try:
        from supabase import create_client

        return create_client(url, key)

    except Exception as e:
        st.error(f"Supabase connection failed: {e}")

        return None