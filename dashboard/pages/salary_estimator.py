import streamlit as st
import pandas as pd
import joblib
import numpy as np

def load_model():
    model = joblib.load('../models/salary_model.pkl')
    le_wf = joblib.load('../models/le_work_format.pkl')
    le_et = joblib.load('../models/le_employment_type.pkl')
    return model, le_wf, le_et

TOP_SKILLS = ['Excel', 'Кыргызский', 'Русский', '1С', 'CRM', 'KPI',
              'Английский', 'MS Office', 'Word', 'SQL', 'API', 'BI',
              'Google Sheets', 'SMM', 'Bitrix']

EXPERIENCE_MAP = {'не требуется': 0, '1–3 года': 1, '3–6 лет': 2, 'более 6 лет': 3}

def render(engine):
    st.title("Salary Estimator")
    st.write("Estimate your expected salary range based on experience and skills.")
    st.warning("⚠️ This model is trained on 263 salary data points. Treat results as a rough range, not a precise prediction.")

    model, le_wf, le_et = load_model()

    col1, col2, col3 = st.columns(3)
    with col1:
        experience = st.selectbox("Experience level", list(EXPERIENCE_MAP.keys()))
    with col2:
        work_format = st.selectbox("Work format", le_wf.classes_)
    with col3:
        employment_type = st.selectbox("Employment type", le_et.classes_)

    selected_skills = st.multiselect("Select your skills", TOP_SKILLS)

    if st.button("Estimate salary"):
        exp_enc = EXPERIENCE_MAP[experience]
        wf_enc = le_wf.transform([work_format])[0]
        et_enc = le_et.transform([employment_type])[0]

        skill_features = [1 if s in selected_skills else 0 for s in TOP_SKILLS]
        feature_names = ['experience_encoded', 'work_format_encoded', 'employment_type_encoded'] + TOP_SKILLS
        features = pd.DataFrame([[exp_enc, wf_enc, et_enc] + skill_features], columns=feature_names)
        prediction = model.predict(features)[0]
        mae = 17080

        st.success(f"Estimated salary range: **{int(prediction - mae):,} — {int(prediction + mae):,} сом/month**")
        st.caption(f"Point estimate: {int(prediction):,} сом | Margin of error: ±{mae:,} сом")