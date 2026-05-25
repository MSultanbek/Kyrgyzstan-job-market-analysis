import json
import time
import os
from playwright.sync_api import sync_playwright
from crawler import scrape_job_urls
from parser import parse_vacancy

KEYWORDS = [
    # ── IT / Software Development ──────────────────────────────
    "Python Developer", "Java Developer", "JavaScript Developer",
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Mobile Developer", "iOS Developer", "Android Developer",
    "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer",
    "Software Engineer", "QA Engineer", "QA Automation Engineer",
    "System Architect", "Solution Architect", "Tech Lead",
    "Разработчик Python", "Разработчик Java", "Разработчик JavaScript",
    "Фронтенд разработчик", "Бэкенд разработчик", "Фулстек разработчик",
    "Мобильный разработчик", "iOS разработчик", "Android разработчик",
    "DevOps инженер", "Системный архитектор", "Тимлид",
    "1С разработчик", "1С программист",

    # ── Data Science / Analytics / AI ─────────────────────────
    "Data Scientist", "Data Analyst", "Data Engineer",
    "Machine Learning Engineer", "ML Engineer", "AI Engineer",
    "Business Intelligence Analyst", "BI Developer",
    "Big Data Engineer", "NLP Engineer", "Computer Vision Engineer",
    "Аналитик данных", "Инженер данных", "Специалист по машинному обучению",
    "Инженер машинного обучения", "BI аналитик", "Бизнес аналитик",
    "Исследователь данных",

    # ── Cybersecurity ──────────────────────────────────────────
    "Information Security Engineer", "Cybersecurity Analyst",
    "Penetration Tester", "SOC Analyst",
    "Инженер по информационной безопасности", "Специалист ИБ",
    "Пентестер", "Аналитик SOC",

    # ── IT Management ──────────────────────────────────────────
    "Product Manager", "Product Owner", "Project Manager",
    "Scrum Master", "IT Director", "CTO",
    "Продуктовый менеджер", "Владелец продукта", "Проектный менеджер",
    "Скрам мастер", "Директор по ИТ",

    # ── Design / UX ────────────────────────────────────────────
    "UX Designer", "UI Designer", "UX/UI Designer",
    "Graphic Designer", "Motion Designer", "Product Designer",
    "UX исследователь", "Дизайнер интерфейсов", "Графический дизайнер",
    "Моушн дизайнер", "Веб дизайнер",

    # ── Finance / Banking / Accounting ─────────────────────────
    "Financial Analyst", "Financial Controller", "CFO",
    "Accountant", "Chief Accountant", "Auditor",
    "Risk Manager", "Compliance Officer", "Treasury Manager",
    "Investment Analyst", "Credit Analyst",
    "Финансовый аналитик", "Финансовый контролер", "Финансовый директор",
    "Бухгалтер", "Главный бухгалтер", "Аудитор",
    "Риск менеджер", "Специалист по комплаенс", "Казначей",
    "Инвестиционный аналитик", "Кредитный аналитик",
    "Экономист", "Финансист",

    # ── Marketing / Advertising ────────────────────────────────
    "Marketing Manager", "Digital Marketing Manager", "SEO Specialist",
    "SMM Manager", "Content Manager", "Copywriter",
    "Performance Marketing Manager", "PPC Specialist", "Brand Manager",
    "PR Manager", "Email Marketing Specialist",
    "Менеджер по маркетингу", "Диджитал маркетолог", "SEO специалист",
    "SMM менеджер", "Контент менеджер", "Копирайтер",
    "Бренд менеджер", "PR менеджер", "Таргетолог",

    # ── Sales / Business Development ───────────────────────────
    "Sales Manager", "Account Manager", "Key Account Manager",
    "Business Development Manager", "Sales Director",
    "Менеджер по продажам", "Аккаунт менеджер",
    "Менеджер по работе с ключевыми клиентами",
    "Менеджер по развитию бизнеса", "Директор по продажам",
    "Торговый представитель",

    # ── HR / Recruitment ───────────────────────────────────────
    "HR Manager", "HR Business Partner", "HR Director",
    "Recruiter", "Talent Acquisition Specialist",
    "HR Generalist", "L&D Specialist", "Compensation & Benefits Specialist",
    "HR менеджер", "HR бизнес партнер", "Директор по персоналу",
    "Рекрутер", "Специалист по подбору персонала",
    "Специалист по обучению и развитию",

    # ── Legal ──────────────────────────────────────────────────
    "Lawyer", "Legal Counsel", "Corporate Lawyer",
    "Contract Specialist", "Compliance Specialist",
    "Юрист", "Корпоративный юрист", "Правовой советник",
    "Специалист по договорной работе", "Юрисконсульт",

    # ── Engineering / Manufacturing ────────────────────────────
    "Process Engineer", "Mechanical Engineer", "Electrical Engineer",
    "Civil Engineer", "Structural Engineer", "Industrial Engineer",
    "Quality Engineer", "Production Manager", "Plant Manager",
    "Технолог", "Инженер технолог", "Механик", "Электрик",
    "Инженер по качеству", "Начальник производства", "Главный инженер",
    "Конструктор", "Инженер-конструктор",

    # ── Construction / Architecture ────────────────────────────
    "Architect", "Construction Manager", "Site Manager",
    "Estimator", "BIM Engineer",
    "Архитектор", "Прораб", "Сметчик", "BIM специалист",
    "Инженер строитель", "Менеджер по строительству",

    # ── Logistics / Supply Chain ───────────────────────────────
    "Logistics Manager", "Supply Chain Manager", "Warehouse Manager",
    "Procurement Manager", "Purchasing Specialist", "Freight Forwarder",
    "Менеджер по логистике", "Начальник склада", "Специалист ВЭД",
    "Менеджер по закупкам", "Специалист по закупкам",
    "Логист", "Экспедитор",

    # ── Healthcare / Medicine ──────────────────────────────────
    "Doctor", "Physician", "Nurse", "Pharmacist",
    "Medical Representative", "Clinical Research Associate",
    "Врач", "Медицинская сестра", "Фармацевт",
    "Медицинский представитель", "Клинический исследователь",

    # ── Education / Training ───────────────────────────────────
    "Teacher", "Trainer", "Corporate Trainer", "E-learning Developer",
    "Преподаватель", "Учитель", "Тренер", "Корпоративный тренер",
    "Методист", "Куратор",

    # ── Customer Support ───────────────────────────────────────
    "Customer Support Specialist", "Customer Success Manager",
    "Call Center Operator", "Help Desk Specialist",
    "Специалист поддержки", "Оператор колл центра",
    "Менеджер по работе с клиентами", "Специалист хелпдеск",

    # ── Administrative / Office ────────────────────────────────
    "Office Manager", "Executive Assistant", "Personal Assistant",
    "Secretary", "Administrator",
    "Офис менеджер", "Личный помощник", "Помощник руководителя",
    "Секретарь", "Административный менеджер",

    # ── General / Cross-industry ───────────────────────────────
    "Стажёр", "Intern", "Junior", "Middle", "Senior",
    "Удалённая работа", "Remote", "Частичная занятость", "Part-time",
]


def main():
    results = []
    success_count = 0
    error_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for keyword in KEYWORDS:
            print(f"\n--- Scraping keyword: {keyword} ---")
            urls = scrape_job_urls(page, keyword, max_pages=3)

            for url in urls:
                try:
                    vacancy = parse_vacancy(page, url)
                    results.append(vacancy)
                    success_count += 1
                except Exception as e:
                    print(f"Error parsing {url}: {e}")
                    error_count += 1
                time.sleep(0.5)

        browser.close()

    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'vacancies_all.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"\nScraping complete. Success: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    main()