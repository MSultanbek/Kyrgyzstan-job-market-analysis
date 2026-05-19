import json
import time
import os
from playwright.sync_api import sync_playwright
from crawler import scrape_job_urls
from parser import parse_vacancy

KEYWORDS = [
    "аналитик", "программист", "бухгалтер", "менеджер",
    "маркетолог", "финансист", "юрист", "дизайнер",
    "разработчик", "экономист",
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