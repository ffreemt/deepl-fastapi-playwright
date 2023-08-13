# pylint: disable=invalid-name, duplicate-code, no-name-in-module, broad-except, line-too-long
r"""
Run deepl-fastapi-pw.

Test from the command line:
```bash

curl -XPOST http://127.0.0.1:8001/text/ -d"{\\"text\\": \\"this is a test\\", \\"to_lang\\": \\"zh\\"}"

curl "http://127.0.0.1:8001/text/?q=test%20this&to_lang=zh"
```
"""
import asyncio
import os
from signal import SIG_DFL, SIGINT, signal
from textwrap import dedent
from typing import Optional

# import nest_asyncio
# import portalocker
import uvicorn
from fastapi import FastAPI, Query

# import logzero
from logzero import logger
from pydantic import BaseModel

from deepl_fastapi_pw import __version__

# from deepl_scraper_pw.deepl_tr import deepl_tr
# from get_pwbrowser_sync.get_pwbrowser_sync import get_pwbrowser_sync
from deepl_fastapi_pw.deepl_tr import deepl_tr
from deepl_fastapi_pw.get_pwbrowser import get_pwbrowser

arun = asyncio.get_event_loop().run_until_complete

# lazy loading LOOP, wait for run_uvicorn to start first
# import lazy_import
# get_ppbrowser = lazy_import.lazy_module(get_ppbrowser)

port = 8001
# nest_asyncio.apply()  # need this for the whole thing to work


async def get_page():
    """Get a page."""
    try:
        # browser = get_pwbrowser_sync()
        browser = await get_pwbrowser()
    except Exception as exc:
        logger.error(exc)
        raise
    try:
        page = await browser.new_page()
    except Exception as exc:
        logger.error(exc)
        raise

    url = r"https://www.deepl.com/translator"
    try:
        await page.goto(url, timeout=16 * 1000)
    except Exception as exc:
        logger.error(exc)
        raise

    return page


LOOP = asyncio.get_event_loop()
PAGE = LOOP.run_until_complete(get_page())

descr = f"""curl -XPOST http://127.0.0.1:{port}/text/ -d '\u007b"text": "this is a test", "to_lang": "zh" \u007d'"""


class Text(BaseModel):  # pylint: disable=too-few-public-methods
    """Define Text model."""

    text: str
    from_lang: Optional[str] = None
    to_lang: Optional[str] = None
    description: Optional[str] = None


app = FastAPI(
    title="deepl-fastapi-pw",
    version=__version__,
    description=__doc__,
)


@app.post("/text/")
def post_text(q: Text):
    """
    Post to /text/.

    Post -d '\u007b"text": "this is a test", "to_lang": "zh" \u007d'
    to http://127.0.0.1:{port}/text/
    """
    text = q.text
    to_lang = q.to_lang
    from_lang = q.from_lang
    logger.debug("text: %s", text)

    # _ = sent_corr(text1, text2)
    try:
        # _ = await deepl_tr(
        _ = arun(
            deepl_tr(
                text,
                from_lang,
                to_lang,
                page=PAGE,
                headless=False,
            )
        )
    except Exception as exc:
        logger.exception(exc)
        _ = {"error": True, "message": str(exc)}

    return {"q": q, "result": _}


@app.get("/text/")
# async def get_text(
# q: Optional[str] = Query(
def get_text(
    q: str = Query(
        # None,
        "",
        max_length=5000,
        min_length=0,
        title="text to translate",
        description=(
            dedent(
                """
            paragraphs will be preserved.
            """.strip()
            )
        ),
    ),
    from_lang: Optional[str] = None,
    to_lang: Optional[str] = "zh",
):
    r"""
    Get text.

    curl "http://127.0.0.1:8001/text/?q=test%20this&to_lang=zh"

    Does not seem work, 'playwright\_impl\_sync_base.py... cannot switch to a different thread' TODO
    """
    result = {
        "q": q,
        "from_lang": from_lang,
        "to_lang": to_lang,
    }
    try:
        # trtext = await deepl_tr(
        trtext = arun(
            deepl_tr(
                q,
                from_lang,
                to_lang,
                page=PAGE,
            )
        )
    except Exception as exc:
        logger.exception(exc)
        trtext = str(exc)

    result.update({"trtext": trtext})
    result.update({"translation": trtext})

    logger.debug("result: %s", result)

    return result


def run_uvicorn():
    """
    Run uvicor.

    Must be run from a different file, e.g., run_uvicorn.py
    """
    uvicorn.run(
        # app="deepl_fastapi.deepl_server:app",
        app=app,  # this should work with python -m deepl_fastapi.deepl_server_async
        # host="0.0.0.0",
        port=port,
        # debug=True,
        # reload=True,
        # workers=2,
        # loop="asyncio",  # default "auto"
        # loop="uvloop",  # posix (linux and mac) only
    )


def main():
    """Start run_uvicorn."""
    logger.info("pid: %s", os.getpid())

    signal(SIGINT, SIG_DFL)
    print("ctrl-C to interrupt, visit http://...:../docs for api docs")

    run_uvicorn()


if __name__ == "__main__":
    main()

    # uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("app.app:app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)

    # uvicorn deepl_fastapi.deepl_server:app --reload
    # works with nest_asyncio

    _ = """
    deepl_scraper_pw.deel_tr is sync

    python -c "from deepl_fastapi_pw import deepl_server; import nest_asyncio; nest_asyncio.apply(); deepl_server.run_uvicorn()"
    python -c "from deepl_fastapi_pw import deepl_server; deepl_server.run_uvicorn()"

    greenlet.error: cannot switch to a different thread
    # import nest_asyncio
    # import sys
    """
