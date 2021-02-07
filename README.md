# Epic Games Bot

[![pypi](https://img.shields.io/pypi/v/epic-games-bot)](https://pypi.org/project/epic-games-bot)
![pyversions](https://img.shields.io/pypi/pyversions/epic-games-bot)
[![ci](https://github.com/george-lim/epic-games-bot-python/workflows/CI/badge.svg)](https://github.com/george-lim/epic-games-bot-python/actions)
[![license](https://img.shields.io/github/license/george-lim/epic-games-bot-python)](https://github.com/george-lim/epic-games-bot-python/blob/main/LICENSE)

## [Usage](#usage) | [Features](#features) | [Examples](#examples) | [CI/CD](#cicd)

Epic Games Bot is a Python library to purchase free promotional offers on Epic Games with the [Playwright API](https://microsoft.github.io/playwright-python).

## Usage

```bash
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

### Purchase free promotional offers (synchronously)

This snippet logs into Epic Games, purchases free promotional offers, and persists all login cookies to a file. It will prioritize login cookies over account credentials for authentication.

```python
import json
from pathlib import Path

from epic_games_bot import EpicGamesBot
from playwright.sync_api import sync_playwright


def run(playwright):
    username = "test@example.com"
    password = "********"

    cookies_path = Path("/tmp/cookies.json")

    browser = None

    try:
        browser = playwright.firefox.launch()
        page = browser.new_page()

        bot = EpicGamesBot(page)

        if cookies_path.exists():
            cookies = json.loads(cookies_path.read_text())
            bot.log_in(cookies)
        else:
            bot.log_in(None, username, password)

        purchased_offer_urls = bot.purchase_free_promotional_offers()

        [print(url) for url in purchased_offer_urls]

        cookies_path.write_text(json.dumps(bot.cookies))

        browser.close()
    except Exception:
        if browser:
            browser.close()

        raise


with sync_playwright() as playwright:
    run(playwright)
```

### Purchase free promotional offers (asynchronously)

This snippet logs into Epic Games, purchases free promotional offers, and persists all login cookies to a file. It will prioritize login cookies over account credentials for authentication.

```python
import asyncio
import json
from pathlib import Path

from epic_games_bot import EpicGamesBot
from playwright.async_api import async_playwright


async def run(playwright):
    username = "test@example.com"
    password = "********"

    cookies_path = Path("/tmp/cookies.json")

    browser = None

    try:
        browser = await playwright.firefox.launch()
        page = await browser.new_page()

        bot = EpicGamesBot(page)

        if cookies_path.exists():
            cookies = json.loads(cookies_path.read_text())
            await bot.async_log_in(cookies)
        else:
            await bot.async_log_in(None, username, password)

        purchased_offer_urls = await bot.async_purchase_free_promotional_offers()

        [print(url) for url in purchased_offer_urls]

        cookies_path.write_text(json.dumps(await bot.cookies))

        await browser.close()
    except Exception:
        if browser:
            await browser.close()

        raise


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
```

## CI/CD

### Secrets

```yaml
PYPI_USERNAME: __token__
PYPI_PASSWORD: "********"

TESTPYPI_USERNAME: __token__
TESTPYPI_PASSWORD: "********"
```

These secrets must exist in the repository for `CD` workflows to publish the PyPI package.
