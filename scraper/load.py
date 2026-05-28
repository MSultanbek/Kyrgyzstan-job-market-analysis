import json
import os
import re
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

DATABASE_URL = 'postgresql://postgres.bcvqmcudccgqzivpqymh:Fnecf6575020612!@aws-1-ap-northeast-2.pooler.supabase.com:5432/postgres'
engine = create_engine(DATABASE_URL)

RUSSIAN_MONTHS = {
    "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
    "мая": 5, "июня": 6, "июля": 7, "августа": 8,
    "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
}

RAW_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


SKILLS = {
    # ── Productivity & Office ──────────────────────────────────────────────
    "Excel":                r"\bexcel\b",
    "Word":                 r"\bword\b",
    "PowerPoint":           r"\bpowerpoint\b",
    "MS Office":            r"ms office|microsoft office",
    "Google Sheets":        r"google sheets|гугл\s*таблиц",
    "Power Query":          r"power\s*query",
    "Power Pivot":          r"power\s*pivot",

    # ── Business Intelligence & Analytics ─────────────────────────────────
    "BI":                   r"\bbi\b",
    "Power BI":             r"power\s*bi",
    "Tableau":              r"\btableau\b",
    "Looker":               r"\blooker\b",
    "Google Analytics":     r"google analytics",
    "Яндекс.Метрика":       r"яндекс[\.\s]*метрик",
    "Google Ads":           r"google ads",
    "Meta Ads":             r"meta ads|facebook ads",
    "TikTok Ads":           r"tiktok\s*ads",
    "SEO":                  r"\bseo\b",
    "SMM":                  r"\bsmm\b",
    "KPI":                  r"\bkpi\b",
    "DAU":                  r"\bdau\b",
    "MAU":                  r"\bmau\b",
    "CJM":                  r"\bcjm\b",

    # ── ERP, CRM & Business Platforms ─────────────────────────────────────
    "CRM":                  r"\bcrm\b",
    "ERP":                  r"\berp\b",
    "1С":                   r"1[сc][\s:\-]|1с\b|1c\b",
    "SAP":                  r"\bsap\b",
    "Bitrix":               r"bitrix|битрикс",
    "HubSpot":              r"\bhubspot\b",
    "Wildberries":          r"wildberries|вайлдберриз|\bwb\b",

    # ── Databases ─────────────────────────────────────────────────────────
    "SQL":                  r"\bsql\b",
    "PostgreSQL":           r"\bpostgresql\b",
    "MySQL":                r"\bmysql\b",
    "MS SQL":               r"\bms\s*sql\b",
    "Redis":                r"\bredis\b",
    "Elasticsearch":        r"\belasticsearch\b",
    "Firebase":             r"\bfirebase\b",
    "NoSQL":                r"\bnosql\b",
    "ELK Stack":            r"\belk\b",

    # ── Programming Languages ─────────────────────────────────────────────
    "Python":               r"\bpython\b",
    "JavaScript":           r"\bjavascript\b",
    "TypeScript":           r"\btypescript\b",
    "Java":                 r"\bjava\b(?!script)",
    "PHP":                  r"\bphp\b",
    "C#":                   r"c#",
    "C++":                  r"c\+\+",
    "Swift":                r"\bswift\b",
    "Kotlin":               r"\bkotlin\b",

    # ── Frameworks & Runtimes ─────────────────────────────────────────────
    "React":                r"\breact\b",
    "Vue.js":               r"\bvue\.?js\b|\bvuejs\b",
    "Node.js":              r"\bnode\.?js\b",
    "Django":               r"\bdjango\b",
    "FastAPI":              r"\bfastapi\b",
    "Flask":                r"\bflask\b",
    "Spring":               r"\bspring\b",
    "Symfony":              r"\bsymfony\b",
    "ASP.NET":              r"\basp\.net\b",
    ".NET":                 r"(?<![a-z])\.net\b",

    # ── Data Science & ML ─────────────────────────────────────────────────
    "Pandas":               r"\bpandas\b",
    "Selenium":             r"\bselenium\b",

    # ── DevOps & Cloud ────────────────────────────────────────────────────
    "Docker":               r"\bdocker\b",
    "Docker Compose":       r"docker\s*compose",
    "Kubernetes":           r"\bkubernetes\b|\bk8s\b",
    "Linux":                r"\blinux\b",
    "Git":                  r"\bgit\b",
    "GitLab":               r"\bgitlab\b",
    "GitHub":               r"\bgithub\b",
    "AWS":                  r"\baws\b",
    "Azure":                r"\bazure\b",
    "GCP":                  r"\bgcp\b|google cloud",
    "CI/CD":                r"\bci/cd\b|\bcicd\b",
    "Rancher":              r"\brancher\b",
    "OpenTelemetry":        r"\bopentelemetry\b",

    # ── Messaging & API Protocols ─────────────────────────────────────────
    "Kafka":                r"\bkafka\b",
    "RabbitMQ":             r"\brabbitmq\b",
    "REST API":             r"\brest\s*api\b|\brestful\b",
    "API":                  r"\bapi\b",
    "GraphQL":              r"\bgraphql\b",
    "gRPC":                 r"\bgrpc\b",

    # ── Web & Frontend ────────────────────────────────────────────────────
    "HTML":                 r"\bhtml\b",
    "CSS":                  r"\bcss\b",
    "UI/UX":                r"\bui\b|\bux\b|ui/ux",

    # ── Mobile ────────────────────────────────────────────────────────────
    "Android":              r"\bandroid\b",
    "iOS":                  r"\bios\b(?!\s*\d)",

    # ── Design & Creative ─────────────────────────────────────────────────
    "Figma":                r"\bfigma\b",
    "Canva":                r"\bcanva\b",
    "Adobe Photoshop":      r"photoshop",
    "Adobe Illustrator":    r"\billustrator\b",
    "Adobe InDesign":       r"\bindesign\b",
    "Adobe Premiere":       r"\bpremiere\b",
    "Adobe After Effects":  r"\bafter\s*effects\b",
    "CorelDRAW":            r"\bcorel\b",
    "Blender":              r"\bblender\b",
    "3ds Max":              r"\b3ds\s*max\b",

    # ── Architecture & Engineering ────────────────────────────────────────
    "AutoCAD":              r"\bautocad\b",
    "Revit":                r"\brevit\b",
    "ArchiCAD":             r"\barchicad\b",
    "SketchUp":             r"\bsketchup\b",

    # ── Project Management & Collaboration ────────────────────────────────
    "Jira":                 r"\bjira\b",
    "Confluence":           r"\bconfluence\b",
    "Notion":               r"\bnotion\b",
    "Trello":               r"\btrello\b",
    "Miro":                 r"\bmiro\b",
    "YouTrack":             r"\byoutrack\b",
    "Agile":                r"\bagile\b",
    "SCRUM":                r"\bscrum\b",
    "Kanban":               r"\bkanban\b",
    "UML":                  r"\buml\b",
    "BPMN":                 r"\bbpmn\b",
    "SDLC":                 r"\bsdlc\b",

    # ── Finance & Accounting Standards ────────────────────────────────────
    "МСФО":                 r"\bмсфо\b",

    # ── AI Tools ──────────────────────────────────────────────────────────
    "ChatGPT":              r"\bchatgpt\b|chat gpt",
    "Claude AI":            r"\bclaude\b",

    # ── Languages ─────────────────────────────────────────────────────────
    "Русский":              r"русск",
    "Английский":           r"английск",
    "Кыргызский":           r"кыргызск",
    "Казахский":            r"казахск",
    "Турецкий":             r"турецк",
    "Немецкий":             r"немецк",
    "Китайский":            r"китайск",
    "Японский":             r"японск",
}

def parse_salary(salary_raw):
    if not salary_raw or pd.isna(salary_raw):
        return None, None, None, None, None
    salary_raw = str(salary_raw).replace('\xa0', ' ').replace('\u202f', ' ')
    patterns = {
        'from_to': r'от\s*([\d\s]+)\s*до\s*([\d\s]+)\s*(сом|\$|USD|₽)?',
        'from_only': r'от\s*([\d\s]+)\s*(сом|\$|USD|₽)?',
        'to_only': r'до\s*([\d\s]+)\s*(сом|\$|USD|₽)?',
    }
    currency = None
    for cur in ['сом', '$', 'USD', '₽']:
        if cur in salary_raw:
            currency = cur
            break
    m = re.search(patterns['from_to'], salary_raw, re.IGNORECASE)
    if m:
        s_from = int(m.group(1).replace(' ', ''))
        s_to = int(m.group(2).replace(' ', ''))
        return s_from, s_to, currency, 'месяц', 'до вычета налогов'
    m = re.search(patterns['from_only'], salary_raw, re.IGNORECASE)
    if m:
        return int(m.group(1).replace(' ', '')), None, currency, 'месяц', 'до вычета налогов'
    m = re.search(patterns['to_only'], salary_raw, re.IGNORECASE)
    if m:
        return None, int(m.group(1).replace(' ', '')), currency, 'месяц', 'до вычета налогов'
    return None, None, None, None, None

def parse_date(date_raw):
    if not date_raw or pd.isna(date_raw):
        return None
    try:
        m = re.search(r'(\d+)\s+(\w+)\s+(\d{4})', str(date_raw))
        if m:
            day = int(m.group(1))
            month = RUSSIAN_MONTHS.get(m.group(2).lower())
            year = int(m.group(3))
            if month:
                return datetime(year, month, day)
    except:
        pass
    return None

def clean_experience(val):
    if pd.isna(val):
        return None
    val = str(val).replace('Опыт работы: ', '').strip()
    return val

def clean_work_format(val):
    if pd.isna(val):
        return None
    return str(val).replace('Формат работы: ', '').strip()

def clean_employment_type(val):
    if pd.isna(val):
        return None
    return str(val).replace('\n', ' / ').strip()

def clean_company(val):
    if pd.isna(val):
        return None
    return str(val).replace('\xa0', ' ').strip()

def extract_skills(description):
    if not description or pd.isna(description):
        return []
    found = []
    for skill, pattern in SKILLS.items():
        if re.search(pattern, str(description), re.IGNORECASE):
            found.append(skill)
    return found


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    print(f"Loaded {len(df)} rows from {filepath}")
    return df


def clean_df(df):
    df['salary_from'], df['salary_to'], df['currency'], \
    df['salary_period'], df['payment_type'] = zip(*df['salary'].apply(parse_salary))

    df['date_posted'] = df['date_raw'].apply(parse_date)
    df['experience_required'] = df['experience'].apply(clean_experience)
    df['work_format'] = df['work_format'].apply(clean_work_format)
    df['employment_type'] = df['employment_type'].apply(clean_employment_type)
    df['company'] = df['company'].apply(clean_company)
    df['skills_found'] = df['description'].apply(extract_skills)

    df = df.dropna(subset=['url'])
    df = df.drop_duplicates(subset=['url'])

    print(f"Cleaned: {len(df)} rows remaining")
    return df


def load_to_db(df):
    def get_or_create_map(table, label_col, values):
        existing = pd.read_sql(
            f"SELECT id, {label_col} FROM {table}", engine
        )
        existing_map = dict(zip(existing[label_col], existing['id']))
        new_vals = [v for v in values.dropna().unique() if v not in existing_map]
        if new_vals:
            new_df = pd.DataFrame(new_vals, columns=[label_col])
            new_df.to_sql(table, engine, if_exists='append', index=False)
            updated = pd.read_sql(f"SELECT id, {label_col} FROM {table}", engine)
            existing_map = dict(zip(updated[label_col], updated['id']))
        return existing_map

    company_map     = get_or_create_map('companies', 'company_name', df['company'])
    period_map      = get_or_create_map('salary_periods', 'label', df['salary_period'])
    payment_map     = get_or_create_map('payment_types', 'label', df['payment_type'])
    employment_map  = get_or_create_map('employment_types', 'label', df['employment_type'])
    work_format_map = get_or_create_map('work_formats', 'label', df['work_format'])

    df['company_id']        = df['company'].map(company_map)
    df['salary_period_id']  = df['salary_period'].map(period_map)
    df['payment_type_id']   = df['payment_type'].map(payment_map)
    df['employment_type_id']= df['employment_type'].map(employment_map)
    df['work_format_id']    = df['work_format'].map(work_format_map)

    vacancies_df = df[[
        'url', 'title', 'salary_from', 'salary_to', 'currency',
        'company_id', 'salary_period_id', 'payment_type_id',
        'employment_type_id', 'work_format_id',
        'experience_required', 'description', 'date_posted'
    ]].copy()

    with engine.connect() as conn:
        existing_urls = {row[0] for row in conn.execute(text("SELECT url FROM vacancies"))}

    new_df = vacancies_df[~vacancies_df['url'].isin(existing_urls)].copy()
    print(f"New vacancies to insert: {len(new_df)}")

    new_df = new_df[new_df['title'].notna()].copy()
    print(f"After filtering nulls: {len(new_df)} rows to insert")

    inserted = 0
    with engine.begin() as conn:
        for _, row in new_df.iterrows():
            row_dict = {k: (None if pd.isna(v) else v) for k, v in row.items()}
            conn.execute(text("""
                INSERT INTO vacancies (url, title, salary_from, salary_to, currency,
                    company_id, salary_period_id, payment_type_id,
                    employment_type_id, work_format_id,
                    experience_required, description, date_posted)
                VALUES (:url, :title, :salary_from, :salary_to, :currency,
                    :company_id, :salary_period_id, :payment_type_id,
                    :employment_type_id, :work_format_id,
                    :experience_required, :description, :date_posted)
                ON CONFLICT (url) DO NOTHING
            """), row_dict)
            inserted += 1

    print(f"Inserted: {inserted} new vacancies")

    skill_df = pd.read_sql("SELECT id, skill_name FROM skills", engine)
    skill_map = dict(zip(skill_df['skill_name'], skill_df['id']))

    with engine.connect() as conn:
        vacancy_map = {row[1]: row[0] for row in conn.execute(text("SELECT id, url FROM vacancies"))}

    new_skills = set()
    for skill_list in df['skills_found']:
        new_skills.update(skill_list)

    with engine.begin() as conn:
        for skill in new_skills:
            if skill not in skill_map:
                conn.execute(text(
                    "INSERT INTO skills (skill_name) VALUES (:s) ON CONFLICT DO NOTHING"
                ), {"s": skill})

    skill_df = pd.read_sql("SELECT id, skill_name FROM skills", engine)
    skill_map = dict(zip(skill_df['skill_name'], skill_df['id']))

    pairs_inserted = 0
    with engine.begin() as conn:
        for _, row in df.iterrows():
            vid = vacancy_map.get(row['url'])
            if not vid:
                continue
            for skill in row['skills_found']:
                sid = skill_map.get(skill)
                if sid:
                    conn.execute(text("""
                        INSERT INTO vacancy_skills (vacancy_id, skill_id)
                        VALUES (:vid, :sid) ON CONFLICT DO NOTHING
                    """), {"vid": vid, "sid": sid})
                    pairs_inserted += 1

    print(f"Inserted: {pairs_inserted} skill-vacancy pairs")




if __name__ == "__main__":
    for filename in sorted(os.listdir(RAW_DATA_PATH)):
        if filename.endswith('.json'):
            filepath = os.path.join(RAW_DATA_PATH, filename)
            df = load_json(filepath)
            df = clean_df(df)
            load_to_db(df)
    print("Pipeline complete.")