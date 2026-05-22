import streamlit as st

from components.sidebar import render_sidebar


def render_layout(title):

    render_sidebar()

    st.title(title)

    st.divider()