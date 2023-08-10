r"""
Instantiate a playwright chrominium browser.

Respect PWBROWSER_ environ variables in .env

Modified from mypython\get_pwbrowser.py

REPL：
from deepl_fastapi_pw.deepl_tr import deepl_tr
from deepl_fastapi_pw.get_pwbrowser import get_pwbrowser
from deepl_fastapi_pw.deepl_server_async import get_page

import asyncio
import atexit
from pathlib import Path
from typing import Optional, Union

import logzero
from logzero import logger
from playwright.async_api import Browser, async_playwright

# from playwright.sync_api import sync_playwright, Browser
# from get_pwbrowser.config import Settings
from pydantic import AnyUrl, BaseSettings  # pylint: disable=no-name-in-module

arun = asyncio.get_event_loop().run_until_complete
playwright = arun(async_playwright().start())

browser = arun(get_pwbrowser())

# page = arun(browser.new_page())  # works
page = arun(get_page())  # also works

res = arun(deepl_tr("this test", page=page))

"""
# pylint: disable=line-too-long
import asyncio
import atexit
import sys
from pathlib import Path
from typing import Optional, Union

import logzero
from logzero import logger
from playwright.__main__ import main
from playwright.async_api import Browser, async_playwright

# from playwright.sync_api import sync_playwright, Browser
# from get_pwbrowser.config import Settings
from pydantic import AnyUrl, BaseSettings  # pylint: disable=no-name-in-module

# check and install chromium/firefox if necessary, 5.79s
_ = sys.argv[:]  # save
# sys.argv = ["", "install", "firefox"]
sys.argv = ["", "install", "chromium"]
try:
    main()
except SystemExit:
    ...
except Exception as exc_:
    logger.error(exc_)
    raise
finally:  # restore
    sys.argv = _[:]


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """
    Configure params DEBUG HEADFUL PROXY.

    import asyncio
    from playwright.async_api import async_playwright

    async def main():
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch()

        # browser = await playwright.chromium.launch(headless=False)

        # Your code here

        # page = await browser.new_page()
        # await page.goto("https://www.google.com")

        # await browser.close()

    asyncio.run(main())

    """

    debug: bool = False
    headful: bool = False
    proxy: Optional[AnyUrl] = None

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        env_prefix = "PWBROWSER_"
        # extra = "allow"
        env_file = ".env"
        env_file_encoding = "utf-8"  # pydantic doc

        logger.info(
            "env_prefix: %s, env_file: %s", env_prefix, Path(env_file).absolute()
        )


arun = asyncio.get_event_loop().run_until_complete
playwright = arun(async_playwright().start())


@atexit.register
def shutdown():
    """Stop playwright."""
    # pyright type error
    # error: Argument of type "None" cannot be assigned to parameter "future" of type "Awaitable[_T@run_until_complete]"
    # asyncio.get_event_loop().run_until_complete(playwright.stop())


config = Settings()
HEADLESS = not config.headful
DEBUG = config.debug
PROXY = config.proxy


# fmt: off
# def get_pwbrowser(
async def get_pwbrowser(
        headless: bool = HEADLESS,
        verbose: Union[bool, int] = DEBUG,
        proxy: Optional[Union[str, dict]] = PROXY,
        **kwargs
) -> Browser:
    # fmt: on
    """Instantiate a playwright chrominium browser (async)."""
    if isinstance(verbose, bool):
        verbose = 10 if verbose else 20
    logzero.loglevel(verbose)

    kwargs.update({
        "headless": headless,
    })

    if proxy:
        proxy = {"server": proxy}
        kwargs.update({
            "proxy": proxy,
        })

    _ = """
    try:
        # playwright = sync_playwright().start()
        playwright = await async_playwright().start()
    except Exception as exc:
        logger.error(exc)
        raise
    # """

    try:
        browser = await playwright.chromium.launch(**kwargs)
        # browser = playwright.chromium.launch(headless=False)
    except Exception as exc:
        logger.error(exc)
        raise

    return browser
