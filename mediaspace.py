import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import time
import pandas as pd


title_to_m3u8 = {}
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
PLAYLISTURL = os.getenv("PLAYLISTURL")
with sync_playwright() as p:

    browser = p.chromium.launch(headless = True)
    if not os.path.exists("website1.json"):
        context = browser.new_context()
        page = context.new_page()
        page.goto(PLAYLISTURL)
    
    ############ SIGNING IN WHEN LOGIN EXPIRES
        page.get_by_label('NetID@illinois.edu').fill(EMAIL)
        page.get_by_role("button", name="Next").click()
        page.get_by_label('Password').fill(PASSWORD)
        page.get_by_role("button", name="Sign in").click()

    ############ CREATING NEW STATE 
        context.storage_state(path="website1.json")
    else:
        context = browser.new_context(storage_state = "website1.json")
        page = context.new_page()
        page.goto(PLAYLISTURL)

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
    print(len(set(hrefs)))

    for index, vidUrl in enumerate(set(hrefs)):
        page.goto(vidUrl, wait_until="domcontentloaded")
        title = page.locator("h1.entryTitle").inner_text().strip()
        # Wait for play button
        play_btn = page.locator("button.playkit-pre-playback-play-button")
        play_btn.wait_for(state="visible", timeout=15000)

        title = page.locator("h1.entryTitle").inner_text().strip()

        def handle_response(response, video_title=title):
            if ".m3u8" in response.url:
                title_to_m3u8[video_title] = response.url

        page.on("response", handle_response)

        play_btn.click()

        # wait a bit for the request to happen
        page.wait_for_timeout(5000)

        page.remove_listener("response", handle_response)

        print(title_to_m3u8[title])
        print("ITERATION: " + str(index + 1) + "/" + str(len(set(hrefs))))
    df = pd.DataFrame( list(title_to_m3u8.items()),
    columns=["title", "m3u8_url"])
    df.to_csv("mediaspace.csv", index = False)
    print("FINISHED")
    page.close()