import requests
import json
from news_data import news_newformat

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

"""headline_payload = {"iso_date": "2023-01-02T00:00:00"}
requests.post("http://0.0.0.0:8000/database/delete", headers=headers,params=headline_payload)"""


headline_payload = {}
requests.post("http://0.0.0.0:8000/database/update/date", headers=headers,params=headline_payload)
requests.post("http://0.0.0.0:8000/database/update/timezone", headers=headers,params=headline_payload)