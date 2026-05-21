from sqlalchemy import create_engine
import streamlit as st

def get_engine():
    url = st.secrets["DATABASE_URL"]
    return create_engine(url)