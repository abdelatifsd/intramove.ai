import requests
import json

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

payload = {
    "product_id": "prod_N1vFZNiYNDhyM3",
    "quantity": 1,
}

"""response = requests.get("http://0.0.0.0:8000/customers", headers=headers)
print(response.json())
"""
intialize = False

if intialize:
    response = requests.post("http://0.0.0.0:8000/checkout", headers=headers, params=payload)
    print(response.json()["session_id"]["url"])
else: 

    for i in range(50):
        headline_payload = {"headline":"The US stock market is down" ,
                    "datetime":"12/21/2022",
                    "callback_url":"dsdsds",}

        headline_headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'api-key': 'e5bd546aeefb83986a23e750fe28382551632427d5651b546abc3285a8ae3315'
        }

        response = requests.post("http://0.0.0.0:8000/analyze/headline", headers=headline_headers,params=headline_payload)
        print(response.json())
