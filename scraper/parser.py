from playwright.sync_api import Page
from typing import Optional, Dict

def parse_vacancy(page: Page, url: str) -> Dict[str, Optional[str]]:
    """
    Navigates to a specific vacancy URL and extracts structured data.
    Returns a dictionary of fields, with None for any missing elements.
    """
    try:
        # Navigate to the specific listing
        # wait_until="domcontentloaded" speeds things up by not waiting for all ads/trackers
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # Mapping of internal keys to their corresponding data-qa selectors
        # These are common selectors for job boards; adjust if your target site differs.
        selectors = {
            "title": '[data-qa="vacancy-title"]',
            "salary": '[data-qa="vacancy-salary-compensation-type-net"]',
            "company": '[data-qa="vacancy-company-name"]',
            "experience": '[data-qa="work-experience-text"]',
            "employment_type": '[data-qa="common-employment-text"]',
            "work_format": '[data-qa="work-formats-text"]',
            "description": '[data-qa="vacancy-description"]',
            "date_raw": ".bloko-gap.bloko-gap_bottom" 
        }
        
        vacancy_data = {"url": url}
        
        for key, selector in selectors.items():
            element = page.query_selector(selector)
            
            if element:
                # Extract text and clean up whitespace
                vacancy_data[key] = element.inner_text().strip()
            else:
                # Explicitly set to None if the field isn't present in this listing
                vacancy_data[key] = None
                
        return vacancy_data

    except Exception as e:
        print(f"Error parsing vacancy at {url}: {e}")
        return {"url": url, "error": str(e)}

# Example usage for testing purposes:
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        test_page = browser.new_page()
        
        # Replace with a real URL from your crawler results
        sample_url = "https://bishkek.headhunter.kg/vacancy/132663357"
        data = parse_vacancy(test_page, sample_url)
        
        print(data)
        browser.close()