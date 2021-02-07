import os

from epic_games_bot import EpicGamesBot
from playwright.sync_api import sync_playwright


def run(playwright):
    username = os.environ["SCHEDULE_EPIC_GAMES_USERNAME"]
    password = os.environ["SCHEDULE_EPIC_GAMES_PASSWORD"]

    browser = None

    try:
        browser = playwright.firefox.launch()
        page = browser.new_page()

        bot = EpicGamesBot(page)

        bot.log_in(None, username, password)

        purchased_offer_urls = bot.purchase_free_promotional_offers()

        [print(url) for url in purchased_offer_urls]

        browser.close()
    except Exception:
        if browser:
            browser.close()

        raise


with sync_playwright() as playwright:
    run(playwright)
