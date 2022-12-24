import requests
import json

headline_payload = {
    "headline": "The US stock market is down",
    "datetime": "12/21/2022",
    "callback_url": "dsdsds",
}

headline_headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "api-key": "9ae446fdcfa4224b5ab9ac0554a381074a4406836228119ac3deb2ce42c5d793",
}

for i in range(1):

    response = requests.post(
        "http://0.0.0.0:8000/analyze/headline",
        headers=headline_headers,
        params=headline_payload,
    )
    print(response.json())
