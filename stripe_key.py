import requests
import json

headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

payload = {"email": "ron@gmail.com", "name": "ron"}
response = requests.get(
    "http://0.0.0.0:8000/client_key", headers=headers, params=payload
)
print(response.json())
