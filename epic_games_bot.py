import logging

from epicstore_api import EpicGamesStoreAPI

EPIC_GAMES_URL = "https://www.epicgames.com"

PERMISSION_COOKIE = {
    "name": "HAS_ACCEPTED_AGE_GATE_ONCE",
    "value": "true",
    "url": EPIC_GAMES_URL,
}


class EpicGamesBot:
    def __init__(self, page):
        self.page = page
        self._is_logged_in = False

    @property
    def is_logged_in(self):
        return self._is_logged_in

    @property
    def cookies(self):
        return self.page.context.cookies()

    def log_in(self, cookies=None, username=None, password=None, code=None):
        if cookies:
            logging.info("Logging in with cookies...")
            self.page.context.add_cookies(cookies)
            self.page.goto(f"{EPIC_GAMES_URL}/login", wait_until="networkidle")
        elif username and password:
            logging.info("Logging in with account credentials...")
            self.page.context.clear_cookies()

            self.page.goto(f"{EPIC_GAMES_URL}/id/login/epic")
            self.page.type("#email", username)
            self.page.type("#password", password)
            self.page.click("#sign-in:enabled")
            self.page.wait_for_load_state("networkidle")

            if "/mfa" in self.page.url:
                self.page.type("#code", code)
                self.page.press("#code", "Enter")
                self.page.wait_for_load_state("networkidle")

            self.page.context.add_cookies([PERMISSION_COOKIE])
        else:
            raise Exception("missing account credentials")

        user = self.page.wait_for_selector("#user")

        if "loggedIn" not in user.get_attribute("class"):
            raise Exception("authentication failed")

        self._is_logged_in = True

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

    def purchase_free_promotional_offers(self):
        if not self.is_logged_in:
            raise Exception("authentication failed")

        logging.info("Purchasing free promotional offers...")
        purchased_offer_urls = []

        for offer_url in self.list_free_promotional_offers():
            self.page.goto(offer_url)

            purchase_buttons = self.page.query_selector_all(
                "//button[contains(., 'Get')]"
            )

            for purchase_button in purchase_buttons:
                purchase_button.click()
                self.page.click(".btn-primary")
                self.page.wait_for_load_state("networkidle")

            if purchase_buttons:
                purchased_offer_urls.append(offer_url)

        return purchased_offer_urls
