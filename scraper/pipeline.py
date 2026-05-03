import json
import time
import os
from playwright.sync_api import sync_playwright
from crawler import scrape_job_urls
from parser import parse_vacancy

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        urls = scrape_job_urls(page, "аналитик", max_pages=5)
        results = []
        success_count = 0
        error_count = 0

        for url in urls:
            try:
                vacancy = parse_vacancy(page, url)
                results.append(vacancy)
                success_count += 1
            except Exception as e:
                print(f"Error parsing {url}: {e}")
                error_count += 1
            time.sleep(2)

        browser.close()

    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'vacancies.json')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Scraping complete. Success: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    main()