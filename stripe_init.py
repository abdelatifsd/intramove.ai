import requests
import json

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

payload = {
    "product_id": "prod_N1vFZNiYNDhyM3",
    "quantity": 3,
}
response = requests.post(
    "http://0.0.0.0:8000/checkout", headers=headers, params=payload
)
url = response.json()["session_id"]["url"]
print(url)
