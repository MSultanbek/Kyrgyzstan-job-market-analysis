import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_metrics(_engine):
    total = pd.read_sql("SELECT COUNT(*) FROM vacancies", _engine).iloc[0, 0]
    with_salary = pd.read_sql("""
        SELECT COUNT(*) FROM vacancies 
        WHERE salary_from IS NOT NULL AND currency = 'сом' AND salary_from > 5000
    """, _engine).iloc[0, 0]
    avg_salary = pd.read_sql("""
        SELECT ROUND(AVG(salary_from)) FROM vacancies 
        WHERE salary_from IS NOT NULL AND currency = 'сом' AND salary_from > 5000
    """, _engine).iloc[0, 0]
    return total, with_salary, avg_salary

@st.cache_data
def load_skills(_engine):
    return pd.read_sql("""
        SELECT s.skill_name, COUNT(*) AS vacancy_count
        FROM vacancy_skills vs
        JOIN skills s ON vs.skill_id = s.id
        GROUP BY s.skill_name
        ORDER BY vacancy_count DESC
        LIMIT 15
    """, _engine)

@st.cache_data
def load_experience(_engine):
    return pd.read_sql("""
        SELECT experience_required, COUNT(*) AS vacancy_count
        FROM vacancies
        GROUP BY experience_required
        ORDER BY vacancy_count DESC
    """, _engine)

@st.cache_data
def load_salaries(_engine):
    return pd.read_sql("""
        SELECT salary_from FROM vacancies
        WHERE salary_from IS NOT NULL
          AND currency = 'сом'
          AND salary_from > 5000
    """, _engine)

def render(engine):
    st.title("Bishkek Job Market — 2026")
    st.write("Analysis of job vacancies from bishkek.headhunter.kg")

    total, with_salary, avg_salary = load_metrics(engine)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total vacancies", f"{total:,}")
    col2.metric("With salary data", f"{with_salary:,}")
    col3.metric("Avg salary (сом)", f"{int(avg_salary):,}")
    col4.metric("Top skill", "Excel")

    st.divider()
    st.subheader("Most demanded skills")
    skills_df = load_skills(engine)
    st.bar_chart(skills_df.set_index('skill_name')['vacancy_count'].sort_values(ascending=True), horizontal=True)

    st.divider()
    st.subheader("Experience required")
    exp_df = load_experience(engine)
    st.bar_chart(exp_df.set_index('experience_required')['vacancy_count'].sort_values(ascending=True), horizontal=True)

    st.divider()
    st.subheader("Salary distribution (KGS only)")
    salary_df = load_salaries(engine)
    fig = px.histogram(salary_df, x='salary_from', nbins=20,
                       labels={'salary_from': 'Salary (сом)'})
    st.plotly_chart(fig, width='stretch')