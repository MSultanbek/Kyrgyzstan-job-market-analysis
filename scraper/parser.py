from playwright.sync_api import Page
from typing import Optional, Dict

def parse_vacancy(page: Page, url: str) -> Dict[str, Optional[str]]:
    
    try:
        
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        
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
                vacancy_data[key] = element.inner_text().strip()

            else:
                vacancy_data[key] = None
                
        return vacancy_data

    except Exception as e:
        print(f"Error parsing vacancy at {url}: {e}")
        return {"url": url, "error": str(e)}


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        test_page = browser.new_page()
        
        
        sample_url = "https://bishkek.headhunter.kg/vacancy/132663357"
        data = parse_vacancy(test_page, sample_url)
        
        print(data)
        browser.close()