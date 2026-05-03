import time
from playwright.sync_api import sync_playwright

def scrape_job_urls(page, keyword: str, max_pages: int):
    clean_urls = []
    
    for current_page in range(max_pages):
        search_url = f"https://bishkek.headhunter.kg/search/vacancy?text={keyword}&area=2760&page={current_page}"
        print(f"Scanning page {current_page}...")
        
        try:
            page.goto(search_url, wait_until="domcontentloaded")
            selectors = page.query_selector_all('[data-qa="serp-item__title"]')
            
            if not selectors:
                print("No more listings found. Stopping.")
                break
            for element in selectors:
                raw_url = element.get_attribute("href")
                if raw_url:
                    clean_url = raw_url.split('?')[0]
                    if clean_url not in clean_urls:
                        clean_urls.append(clean_url)
            print(f"Found {len(selectors)} items. Sleeping for 3 seconds...")
            time.sleep(3)
        except Exception as e:
            print(f"Error encountered on page {current_page}: {e}")
            break
    
    return clean_urls

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        results = scrape_job_urls(page, "аналитик", max_pages=2)
        browser.close()
    print(f"\nSuccessfully extracted {len(results)} clean URLs:")
    for url in results:
        print(url)