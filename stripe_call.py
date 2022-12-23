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
    "api-key": "a62963b7ed9430029cec2375507735d34c8e3e266d7059551c33341f6474aeea",
}

for i in range(15):

    response = requests.post(
        "http://0.0.0.0:8000/analyze/headline",
        headers=headline_headers,
        params=headline_payload,
    )
    print(response.json())
