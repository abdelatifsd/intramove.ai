import requests
import json

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

headline_payload = {"headline": "US Stocks Regain Ground",
            "callback_url": ""}

article = """Sell-off driven by stronger-than-expected jobs reports faded in the afternoon trading on Friday, with the Dow Jones crossing into the positive territory and the S&P 500 and the Nasdaq closing down only 0.2% and 0.1% respectively. On one hand, the Labor Department's closely watched employment report showed that the economy added 263,000 jobs last month while average hourly earnings unexpectedly rose more than expected cooling expectations that the Federal Reserve will soon slow its tightening campaign. On the other hand, investors took a respite from Fed Chair Jerome Powell's remarks that confirmed rate hikes would slow starting as early as December. On the corporate side, Marvell Technology tumbled as much as 5% after the semiconductor company missed quarterly revenue and earnings estimates. For the week, the Dow ended 0.1% higher, while Nasdaq rose 2.1% and the S&P was up 1%."""
article_payload = {"article": article,
                   "callback_url":""}

#"callback_url": "https://webhook.site/09871e7a-f3b4-4b1e-9d83-a9faf37ae978"}

local = True
if not local: 
    pass #response = requests.post('https://transcribe.repustate.com/transcribe', headers=headers, params=headline_payload)
else:
    response1 = requests.post("http://0.0.0.0:8000/analyze/headline", headers=headers,params=headline_payload)
    response2 = requests.post("http://0.0.0.0:8000/analyze/article", headers=headers,params=article_payload)


# This would print the response in your terminal. You can change it however to access and manupilate the results
print(response1.json())
print(response2.json())