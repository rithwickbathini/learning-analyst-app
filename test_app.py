import streamlit as st

st.set_page_config(
    page_title="Test",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: #0f172a;
    color: white;
}

.stButton > button {
    background: #6366f1;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("CSS Working Test")
st.button("Test Button")