# curl "http://127.0.0.1:8001/text?q=test"
curl -X 'GET' \
  'http://127.0.0.1:8001/text/?q=test&to_lang=zh' \
  -H 'accept: application/json'

curl "http://127.0.0.1:8001/text/?to_lang=zh&q=test"
