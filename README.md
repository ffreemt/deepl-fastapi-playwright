# deepl-fastapi-pw
<!--- repo-name  pypi-name  mod_name func_name --->
[![tests](https://github.com/ffreemt/deepl-fastapi-playwright/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/deepl-fastapi-playwright/actions)
[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-fastapi-pw.svg)](https://badge.fury.io/py/deepl-fastapi-pw)

Your own deepl server via fastapi and playwright, cross-platform (Windows/Linux/MacOs) with API for OmegaT

## Installation
*   Create a virual environment: optional but recommended
    e.g.,
    ```bash
    # Linux and friends
    python3.8 -m venv .venv
    source .venv/bin/activate

    # Windows
    # py -3.8 -m venv .venv
    # .venv\Scripts\activate
    ```

```bash
pip install deepl-fastapi-pw
```
or (if your use poetry)
```bash
poetry add deepl-fastapi-pw
```
or
```
 pip install git+https://github.com/ffreemt/deepl-fastapi-playwright.git
```
or
*   Clone the repo [https://github.com/ffreemt/deepl-fastapi-playwright.git](https://github.com/ffreemt/deepl-fastapi-playwrigh.git)
    ```bash
    git clone https://github.com/ffreemt/deepl-fastapi-playwright.git
    ```
    and `cd deepl-fastapi-playwright`
*   `pip install -r requirements.txt
    * or ``poetry install``

## Usage

*   Start the server

```
python  -m deepl_fastapi_pw
```

Or use uvicorn directly (note the `deepl_server` module, not `run_uvicorn`)
```bash
uvicorn deepl_fastapi_pw.deepl_server_async:app
```

or
```bash
python -m deepl_fastapi_pw.deepl_server_async
```

or run the server on the external net, for example at port 9888
```
uvicorn deepl_fastapi_pw.deepl_server:app --reload --host 0.0.0.0 --port 9888
```

### Explore and consume

Point your browser to [http://127.0.0.1:8001/text/?q=test&to_lang=zh](http://127.0.0.1:8001/text/?q=test&to_lang=zh)

Or in command line:
```bash
python -c "import httpx; print(httpx.get('http://127.0.0.1:8001/text/?to_lang=zh&q=test 1\ntest 2').json())"
# output: {'q': 'test 1\ntest 2', 'from_lang': None, 'to_lang': 'zh', 'trtext': '测试 1\n测试 2', 'translation': '测试 1\n测试 2'}
```

Or in python code (`pip install requests` first)
```python
import requests

# get
url = "http://127.0.0.1:8001/text/?q=test me&to_lang=zh"
print(requests.get(url).json())
# {'q': 'test me', 'from_lang': None, 'to_lang':
# 'zh', 'trtext': '考我', 'translation': '考我'}
```

`'translation'` is there for `OmegaT` plugin. Refer to the `OmegaT Fake MT plugin setup` part
in [https://github.com/ffreemt/deepl-fastapi](https://github.com/ffreemt/deepl-fastapi)
```
# post
text = "test me \n and him"
data = {"text": text, "to_lang": "zh"}
resp = requests.post("http://127.0.0.1:8001/text", json=data)
print(resp.json())
# {'q': {'text': 'test me \n and him', 'from_lang': None,
# 'to_lang': 'zh', 'description': None}, 'result': '考验我 \n  我和他'}
```

### NB
* Text longer than 1500 characters will be trimmed to 1500. This is what the `deepl.com` webpage can handle (used to be 5000 characters).
* The package `deepl-fastapi-pw` is in essence a browser from your local IP (although a proxy can be used, refer to get-pwbroser's doc for setting up). Hence if you send too many requests too frequently, your IP may be blocked by `deepl.com` temporarily, which of course will also disable `deepl-fastapi-pw`.

## Interactive Docs (Swagger UI)

 [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
