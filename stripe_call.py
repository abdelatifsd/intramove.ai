import requests
import json


for i in range(20):
    headline_payload = {
        "headline": "The US stock market is down",
        "datetime": "12/21/2022",
        "callback_url": "dsdsds",
    }

    headline_headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": "f490220303d1b2cd7ae89266926dd09a5d3cfc15b5e06ae9a831c3f33a90cf60",
    }

    response = requests.post(
        "http://0.0.0.0:8000/analyze/headline",
        headers=headline_headers,
        params=headline_payload,
    )
    print(response.json())
