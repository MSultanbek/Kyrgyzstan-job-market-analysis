from playwright.sync_api import sync_playwright
from time import sleep

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()
    page.goto("https://bishkek.headhunter.kg/")
    print(page.title())

    sleep(5)
    browser.close()