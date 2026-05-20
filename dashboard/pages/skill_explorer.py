import streamlit as st
import pandas as pd

@st.cache_data
def load_skills(_engine):
    return pd.read_sql("""
        SELECT s.skill_name, COUNT(*) AS vacancy_count,
               ROUND(AVG(v.salary_from)) AS avg_salary
        FROM vacancy_skills vs
        JOIN skills s ON vs.skill_id = s.id
        JOIN vacancies v ON vs.vacancy_id = v.id
        WHERE v.salary_from IS NOT NULL
          AND v.currency = 'сом'
          AND v.salary_from > 5000
        GROUP BY s.skill_name
        ORDER BY vacancy_count DESC
    """, _engine)

@st.cache_data
def load_all_skills(_engine):
    return pd.read_sql("""
        SELECT DISTINCT s.skill_name
        FROM skills s
        ORDER BY s.skill_name
    """, _engine)['skill_name'].tolist()

def render(engine):
    st.title("Skill Explorer")
    st.write("Select a skill to see its demand and average salary.")

    all_skills = load_all_skills(engine)
    selected = st.selectbox("Choose a skill", all_skills)

    skills_df = load_skills(engine)
    row = skills_df[skills_df['skill_name'] == selected]

    if not row.empty:
        col1, col2 = st.columns(2)
        col1.metric("Listings requiring this skill", int(row['vacancy_count'].values[0]))
        col2.metric("Avg salary when required (сом)", f"{int(row['avg_salary'].values[0]):,}")
    else:
        st.info("No salary data available for this skill.")

    st.divider()
    st.subheader("All skills by demand")
    st.bar_chart(
        skills_df.set_index('skill_name')['vacancy_count'].sort_values(ascending=True),
        horizontal=True
    )