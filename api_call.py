import requests
import json
import news

def magic(batch_date,divider, news_batch):
    split_data = news_batch.split(divider)
    headlines = []
    articles = []
    date = []
    for data in split_data:
        if data != "":
            headlines.append(data.split("\n")[1])
            article = " ".join(data.split("\n")[2:]).replace("\n","")
            articles.append(article)
            date.append(batch_date)

    return headlines, articles

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

"""headline_payload = {"headline": "US Stocks Under Pressure After NFP Report",
                    "datetime":"12/02/2022",
                    "callback_url":} """


news_cache = news.news_cache

for date_and_divider, news_batch in news_cache.items():
    date = date_and_divider.split("-")[0]
    divider = date_and_divider.split("-")[1]

    headlines, articles = magic(date, divider, news_batch)
    assert len(headlines) == len(articles), "length mismatch"
   
    for index in range(len(headlines)):
         headline_payload = {"headline":headlines[index] ,
                    "datetime":date,
                    "callback_url":""}
         requests.post("http://0.0.0.0:8000/analyze/headline", headers=headers,params=headline_payload)

         article_payload = {"article":articles[index] ,
                    "datetime":date,
                    "callback_url":""}
         requests.post("http://0.0.0.0:8000/analyze/article", headers=headers,params=article_payload)
  