import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time


load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
with sync_playwright() as p:

    browser = p.chromium.launch(headless = False)
    context = browser.new_context(storage_state = "website1.json")
    page = context.new_page()

    page.goto("https://mediaspace.illinois.edu/default/channels/view/channelname/STAT\%20433\%20Spring%202025/channelid/368732312")
    

    ############ SIGNING IN WHEN LOGIN EXPIRES
    # page.get_by_label('NetID@illinois.edu').fill(EMAIL)
    # page.get_by_role("button", name="Next").click()
    # page.get_by_label('Password').fill(PASSWORD)
    # page.get_by_role("button", name="Sign in").click()

    ############ CREATING NEW STATE 
    # context.storage_state(path="website1.json")
    time.sleep(10)
    while True:
        # Count current items
        curr_count = page.locator(".galleryItem").count()

        # Try to load next page
        page.evaluate("""
            endlessScrollersPrototype.loadNextPage('channelGallery');
        """)

        time.sleep(3)  # allow network + DOM update

        new_count = page.locator(".galleryItem").count()

        # Stop if nothing new loaded
        if new_count == curr_count:
            break

        prev_count = new_count
    
    links = page.locator("a.item_link")
    count = links.count()
    print("Found", count, "item_link elements")
    hrefs = []

    for i in range(count):
        href = links.nth(i).get_attribute("href")
        if href:
            hrefs.append("https://mediaspace.illinois.edu" + href)
    print(set(hrefs))
    page.pause()
