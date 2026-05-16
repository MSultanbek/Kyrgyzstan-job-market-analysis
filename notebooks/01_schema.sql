create database if not exists hhkg_jobs;
use hhkg_jobs;


CREATE TABLE companies (
    id    SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE payment_types (
    id    SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE employment_types (
    id    SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE work_formats (
    id    SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE salary_periods (
    id    SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE skills (
    id    SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE vacancies (
    id                  SERIAL PRIMARY KEY,
    url                 TEXT NOT NULL UNIQUE,
    title               TEXT NOT NULL,
    salary_from         INTEGER,
    salary_to           INTEGER,
    company_id          INTEGER REFERENCES companies(id),
    salary_period_id    INTEGER REFERENCES salary_periods(id),
    payment_type_id     INTEGER REFERENCES payment_types(id),
    employment_type_id  INTEGER REFERENCES employment_types(id),
    work_format_id      INTEGER REFERENCES work_formats(id),
    experience_required VARCHAR(100),
    description         TEXT,
    date_posted         DATE,
    scraped_at          TIMESTAMP DEFAULT NOW()
);



CREATE TABLE vacancy_skills (
    vacancy_id INTEGER REFERENCES vacancies(id) ON DELETE CASCADE,
    skill_id   INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    PRIMARY KEY (vacancy_id, skill_id)
);