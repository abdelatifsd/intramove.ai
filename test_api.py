import requests
import json

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

headline_payload = {"headline": "TSX Cuts Losses",
            "callback_url": ""}

article = "The S&P/TSX Composite index closed down only 0.2% at the 20,500 level on Friday, as investors were reassessing the monetary policy path. On one hand, stronger-than-expected labor data increased bets that central banks could move more aggressively to tighten policy. The Canadian unemployment rate unexpectedly fell by 0.1 percentage point to 5.1% in November, as unemployment fell by over 20 thousand people and over 10 thousand jobs were added, In the meantime, US payroll data showed that 263 thousand jobs were added to the US economy, well above expectations of 200 thousand. Still, on the other hand, investors took a respite from Fed Chair Jerome Powell's remarks that confirmed rate hikes would slow starting as early as December."
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