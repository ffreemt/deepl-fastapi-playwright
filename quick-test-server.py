r"""
Test for curl/httpx/requseets.

# curl "http://127.0.0.1:8001/text/?q=test"
curl -X 'GET' 'http://127.0.0.1:8001/text/?q=test&to_lang=zh' -H 'accept: application/json'.

curl "http://127.0.0.1:8001/text/?to_lang=zh&q=test\nabc"
does not work

curl -X "POST" ^
  "http://127.0.0.1:8001/text/" ^
  -H "accept: application/json" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"test me\ntest him\", \"from_lang\": \"en\", \"to_lang\": \"zh\", \"description\": \"string\"}"


use:

python -c "import httpx; print(httpx.get('http://127.0.0.1:8001/text/?to_lang=de&q=test 1\ntest 2').json())"

run first:
    python -m deepl_fastapi_pw
"""
import httpx

print(httpx.get('http://127.0.0.1:8001/text/?to_lang=de&q=test 1\ntest 2', timeout=20).json())
