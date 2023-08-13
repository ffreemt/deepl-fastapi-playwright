"""Check."""
# pylint: disable=broad-except
import os
from pathlib import Path
from threading import Thread
from time import sleep, time
from urllib.parse import quote

import requests
from logzero import logger

# start the server in a thread
from deepl_fastapi_pw import __main__

# wait for the server to go alive
then = time()
flag = True
while True:
    if time() - then > 300:  # 5 min
        break
    try:
        requests.get("http://127.0.0.1:8001/text/", timeout=2)
        logger.info("Server is up")
        break
    except requests.ConnectTimeout:
        # start server for once
        if flag:
            flag = False
            Thread(target=__main__.main, daemon=True).start()
        continue
    except Exception:
        break

# start the server if not already started

_ = """ start server
lockfile = f'{Path(__file__).parent.parent /  "deepl_server.py.portalocker.lock"}'

# create one if not exist
Path(lockfile).touch(exist_ok=True)
file = open(lockfile)
logger.info("lockfile: %s", lockfile)

try:
    portalocker.lock(file, portalocker.LOCK_EX | portalocker.LOCK_NB)
    locked = False
    portalocker.unlock(file)
except Exception:
    locked = True

logger.debug("locked: %s", locked)
if not locked:
    cwd = Path(__file__).absolute().parent.as_posix()
    executable = f"{sys.executable}"
    if os.name in ["posix"]:  # linux and friends
        cmd = f"nohup python -m deepl_fastapi_pw.run_uvicorn > {cwd}" "/server.out 2>&1 &"
        Popen(cmd, shell=True)
        logger.info(
            "fastapi server running in background, output logged to: %s/server.out",
            cwd,
        )
    else:
        try:
            Popen(f"{executable} -m deepl_fastapi_pw.run_uvicorn", shell=True)
            logger.info(
                "\n\t [%s] fastapi server running in background\n",
                "deepl_fastapi_pw.run_uvicorn",
            )
        except Exception as exc:
            logger.debug(exc)

    # wait for server to come up
    sleep(20)
# """


def test_longtext():
    """Test longtext 2022-07-09.txt."""
    # pdir = Path(__file__).parent
    pdir = Path('tests')
    _ = Path(pdir, "2022-07-09.txt").read_text(encoding="utf8").splitlines()
    text = "\n".join([elm for elm in _ if elm.strip()][1:4])
    text = quote(text)

    logger.info("text: %s", text)

    try:
        # _ = requests.get("http://127.0.0.1:8001/text/?q=test me", verify=False, timeout=5)
        _ = requests.get(f"http://127.0.0.1:8001/text/?q={text}", verify=False, timeout=5)
        res = str(_.json())
    except Exception as exc:
        logger.error(exc)

        try:
            # _ = requests.get("http://127.0.0.1:8001/text/?q=test me", verify=False, timeout=5)
            _ = requests.get(f"http://127.0.0.1:8001/text/?q={text}", verify=False, timeout=5)
            res = str(_.json())
        except Exception as exc_:
            logger.error("2nd try: %s", exc_)
            res = str(exc)
            # somehow Windows test dose not work on github VM
            # it's alright on local Windows 10.
            # TODO: will fix this later
            if os.name.lower() not in ["posix"]:
                # res = "我" + res
                ...

    logger.info("res: %s", res)
    sleep(5)

    assert "人工智能" in res
    # assert False

if __name__ == "__main__":
    try:
        test_longtext()
    except Exception as exc_:
        logger.exception("%s", exc_)
