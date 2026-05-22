import streamlit as st


def page_header(title, subtitle=""):

    st.markdown(f"""
        <div style="padding-bottom:20px;">
            <h1 style="margin-bottom:0;">{title}</h1>
            <p style="color:gray;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)