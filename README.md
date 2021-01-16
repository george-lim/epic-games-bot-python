# Epic Games Bot

[![pypi](https://img.shields.io/pypi/v/epic-games-bot)](https://pypi.org/project/epic-games-bot)
![pyversions](https://img.shields.io/pypi/pyversions/epic-games-bot)
[![ci](https://github.com/george-lim/epic-games-bot-python/workflows/CI/badge.svg)](https://github.com/george-lim/epic-games-bot-python/actions)
[![license](https://img.shields.io/github/license/george-lim/epic-games-bot-python)](https://github.com/george-lim/epic-games-bot-python/blob/main/LICENSE)

## [Usage](#usage) | [Features](#features) | [Examples](#examples) | [CI/CD](#cicd)

Epic Games Bot is a Python library to purchase free promotional offers on Epic Games with the [Playwright API](https://microsoft.github.io/playwright-python).

## Usage

```bash
python3 -m pip install requests
python3 -m pip install epic-games-bot
python3 -m playwright install
```

This installs Epic Games Bot and its dependencies. Once installed, add `import epic_games_bot` to a Python script to begin using Epic Games Bot.

> Note: Epic Games adds aggressive CAPTCHA verification when Chromium is chosen as the headless browser. Firefox is recommended when running Epic Games Bot.

## Features

Epic Games Bot accepts either account credentials or existing login cookies to authenticate the user. It automatically finds and purchases free promotional offers on behalf of the user.

## Examples

### List free promotional offers

This snippet lists free promotional offers on Epic Games.

```python
from epic_games_bot import EpicGamesBot

print(EpicGamesBot.list_free_promotional_offers())
# > ['https://www.epicgames.com/...', ...]
```

### Purchase free promotional offers

This snippet logs into Epic Games and purchases free promotional offers.

```python
from epic_games_bot import EpicGamesBot
from playwright import sync_playwright

username = "test@example.com"
password = "********"
code = None  # 2FA (optional)

with sync_playwright() as api:
    browser = None

    try:
        browser = api.firefox.launch()
        page = browser.newPage()

        bot = EpicGamesBot(page, None, username, password, code)
        purchased_offer_urls = bot.purchase_free_promotional_offers()

        [print(url) for url in purchased_offer_urls]

        browser.close()
    except Exception:
        if browser:
            browser.close()

        raise
```

### Login session persistence

This snippet shows how to persist and restore login sessions with cookies.

```python
cookies_path = pathlib.Path("/tmp/cookies.json")

# Persist `cookies` to `cookies_path`
bot = EpicGamesBot(page, None, username, password, code)
cookies = bot.get_cookies()
cookies_path.write_text(json.dumps(cookies))

# Restore `cookies` from `cookies_path`
cookies = json.loads(cookies_path.read_text())
bot = EpicGamesBot(page, cookies)
```

## CI/CD

### Secrets

```yaml
PYPI_USERNAME: '__token__'
PYPI_PASSWORD: '********'

TESTPYPI_USERNAME: '__token__'
TESTPYPI_PASSWORD: '********'
```

These secrets must exist in the repository for `CD` workflows to publish the PyPI package.
