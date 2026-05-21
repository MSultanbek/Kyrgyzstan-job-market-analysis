# Kyrgyzstan Job Market Intelligence
**Live data pipeline + analytics platform for the Bishkek job market**

Built from scratch using real scraped data from bishkek.headhunter.kg — no public dataset existed for this market.

---

## Key Findings

| Finding | Data |
|---|---|
| Most demanded skill | Excel (163 listings, 19% of all roles) |
| Dominant experience tier | 1–3 years (467 listings, 56% of market) |
| Entry-level avg salary | 37,443 сом/month |
| Senior-level avg salary | 91,111 сом/month |
| Salary premium per tier | ~18,000–20,000 сом |
| Top skill in high-paying roles | KPI (16 listings above 60,000 сом) |

**Minimum viable skill set for 1–3 year roles above 50,000 сом:**
Excel + KPI understanding + CRM + Kyrgyz/Russian language

---

## What This Project Does

A four-tier data pipeline built entirely from scratch:

1. **Scraper** — Playwright-based crawler collects job listings from bishkek.headhunter.kg across 20 search keywords
2. **Pipeline** — Cleans raw JSON, parses salary strings, extracts skills via NLP regex, loads into PostgreSQL
3. **Analytics** — 5 business questions answered with visualizations (EDA notebooks)
4. **Product** — Deployed Streamlit dashboard with skill explorer and ML salary estimator

---

## Dashboard

Three interactive pages:
- **Market Overview** — top skills, salary distribution, experience breakdown
- **Skill Explorer** — select any skill to see demand and average associated salary
- **Salary Estimator** — input experience + skills → predicted salary range

> Salary model: Random Forest Regressor | MAE: 17,080 сом | R²: 0.155
> Trained on 263 verified KGS salary data points

---

## Technical Stack

| Layer | Tools |
|---|---|
| Scraping | Python, Playwright, Chromium |
| Storage | PostgreSQL (normalized schema, 8 tables) |
| Cleaning | Python, pandas, regex |
| NLP | Custom skill extractor (66 skills, regex patterns) |
| ML | scikit-learn Random Forest |
| Dashboard | Streamlit, Plotly |
| Version control | Git, GitHub |

---

## Project Structure

```text
├── scraper/
│   ├── crawler.py               # URL collection with pagination
│   ├── parser.py                # Field extraction via data-qa selectors
│   └── pipeline.py              # End-to-end orchestration
├── notebooks/
│   ├── 01_schema.sql            # SQL script for Creating the Database
│   ├── 02_cleaning.ipynb        # Data cleaning + PostgreSQL loading
│   ├── 03_eda.ipynb             # EDA and business questions
│   └── 04_salary_model.ipynb    # ML salary predictor
├── dashboard/
│   ├── app.py                   # Streamlit entry point
│   └── pages/                   # Modular page components
├── models/                      # Saved ML model
└── visuals/                     # Chart exports
```

---

## How to Run

```bash
git clone https://github.com/MSultanbek/Kyrgyzstan-job-market-analysis
cd Kyrgyzstan-job-market-analysis
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
cd dashboard && streamlit run app.py
```

Requires PostgreSQL running locally with `hhkg_jobs` database.

---

## Author

**Muratbekov Sultanbek** — Applied Mathematics and Informatics, Ala-Too International University, Bishkek
[GitHub](https://github.com/MSultanbek)