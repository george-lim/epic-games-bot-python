import logging

from epicstore_api import EpicGamesStoreAPI

EPIC_GAMES_URL = "https://www.epicgames.com"

PERMISSION_COOKIE = {
    "name": "HAS_ACCEPTED_AGE_GATE_ONCE",
    "value": "true",
    "url": EPIC_GAMES_URL,
}


class EpicGamesBot:
    def __init__(self, page, cookies=None, username=None, password=None, code=None):
        self.page = page

        if cookies:
            logging.info("Logging in with cookies...")
            page.context.addCookies(cookies)
            page.goto(f"{EPIC_GAMES_URL}/login", waitUntil="networkidle")
        elif username and password:
            logging.info("Logging in with account info...")
            page.context.clearCookies()

            page.goto(f"{EPIC_GAMES_URL}/id/login/epic")
            page.type("#email", username)
            page.type("#password", password)
            page.click("#sign-in:enabled")
            page.waitForNavigation()

            if "/mfa" in page.url:
                page.type("#code", code)
                page.press("#code", "Enter")
                page.waitForNavigation()

            page.context.addCookies([PERMISSION_COOKIE])
        else:
            raise Exception("missing authentication info")

        user = page.waitForSelector("#user")

        if "loggedIn" not in user.getAttribute("class"):
            raise Exception("authentication failed")

    @staticmethod
    def list_free_promotional_offers():
        api = EpicGamesStoreAPI()
        free_games = api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]
        offer_urls = []

        for free_game in free_games:
            promotions = free_game.get("promotions")

            if promotions and promotions.get("promotionalOffers"):
                product_slug = free_game["productSlug"].split("/", 1)[0]
                product = api.get_product(product_slug)

                url_patterns = []
                addon_url_patterns = []

                for page in product["pages"]:
                    if page["type"] == "productHome":
                        url_patterns.append(page["_urlPattern"])
                    elif page["type"] in ["addon", "offer"]:
                        addon_url_patterns.append(page["_urlPattern"])

                url_patterns.extend(addon_url_patterns)

                for url_pattern in url_patterns:
                    product_path = url_pattern.replace("productv2", "product")
                    offer_urls.append(f"{EPIC_GAMES_URL}/store/en-US{product_path}")

        return offer_urls

    def get_cookies(self):
        return self.page.context.cookies()

    def purchase_free_promotional_offers(self):
        logging.info("Purchasing free promotional offers...")
        purchased_offer_urls = []

        for offer_url in self.list_free_promotional_offers():
            self.page.goto(offer_url)
            purchase_buttons = self.page.querySelectorAll(
                "//button[contains(., 'Get')]"
            )

            for purchase_button in purchase_buttons:
                purchase_button.click()
                self.page.click(".btn-primary")
                self.page.waitForNavigation()

            if purchase_buttons:
                purchased_offer_urls.append(offer_url)

        return purchased_offer_urls
