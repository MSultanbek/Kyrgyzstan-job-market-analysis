import streamlit as st
from utils.database import get_engine
from pages import overview, skill_explorer, salary_estimator

# FIX: Add client.showSidebarNavigation=False
st.set_page_config(
    page_title="Bishkek Job Market", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide the native multipage sidebar navigation links
st.html(
    """
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    </style>
    """
)

engine = get_engine()

page = st.sidebar.selectbox("Navigate", [
    "Market Overview",
    "Skill Explorer", 
    "Salary Estimator"
])

if page == "Market Overview":
    overview.render(engine)
elif page == "Skill Explorer":
    skill_explorer.render(engine)
elif page == "Salary Estimator":
    salary_estimator.render(engine)