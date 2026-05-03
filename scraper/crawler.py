import time
from playwright.sync_api import sync_playwright

def scrape_job_urls(keyword: str, max_pages: int):
    """
    Scrapes unique URLs from search results based on a keyword.
    """
    clean_urls = []
    
    # We use sync_playwright for a straightforward, linear script
    with sync_playwright() as p:
        # Launching chromium; use headless=False if you want to watch the magic happen
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for current_page in range(max_pages):
            # Construct the URL - using a common pattern for sites utilizing data-qa attributes
            # Adjust the base URL as needed for your specific target
            search_url = f"https://bishkek.headhunter.kg/search/vacancy?text={keyword}&area=2760&page={current_page}"
            
            print(f"Scanning page {current_page}...")
            
            try:
                page.goto(search_url, wait_until="domcontentloaded")
                
                # Select all elements with the specific data-qa attribute
                selectors = page.query_selector_all('[data-qa="serp-item__title"]')
                
                if not selectors:
                    print("No more listings found. Stopping.")
                    break

                for element in selectors:
                    raw_url = element.get_attribute("href")
                    if raw_url:
                        # Strip tracking parameters (everything from '?' onwards)
                        clean_url = raw_url.split('?')[0]
                        
                        # Ensure we don't add duplicates
                        if clean_url not in clean_urls:
                            clean_urls.append(clean_url)

                # Ethical scraping: Don't hammer the server
                print(f"Found {len(selectors)} items. Sleeping for 3 seconds...")
                time.sleep(3)

            except Exception as e:
                print(f"Error encountered on page {current_page}: {e}")
                break

        browser.close()
        
    return clean_urls

if __name__ == "__main__":
    # Quick test run
    results = scrape_job_urls("Аналитик", max_pages=2)
    print(f"\nSuccessfully extracted {len(results)} clean URLs:")
    for url in results:
        print(url)