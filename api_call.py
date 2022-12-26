import requests
import json
from news_data import news_newformat

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

### CHECK THIS FIRST ###
manual = False
### CHECK THIS FIRST ###


if not manual:

    for date, headline_article_dict in news_newformat.news_cache.items():
        
        headlines = headline_article_dict["headlines"]
        articles = headline_article_dict["articles"]

        
        assert len(headlines) == len(articles), "length mismatch"

        for index in range(len(headlines)):
            headline_payload = {"headline":headlines[index] ,
                        "datetime":date,
                        "callback_url":""}
            requests.post("http://0.0.0.0:8000/analyze/headline", headers=headers,params=headline_payload)


    for date, headline_article_dict in news_newformat.news_cache.items():
        
        headlines = headline_article_dict["headlines"]
        articles = headline_article_dict["articles"]

        for index in range(len(headlines)):
            article_payload = {"article":articles[index] ,
                                "datetime":date,
                                "callback_url":""}
            requests.post("http://0.0.0.0:8000/analyze/article", headers=headers,params=article_payload)
else:
    headline_payload = {"headline":"" ,
                        "datetime":"12/07/2022",
                        "callback_url":""}
    requests.post("http://0.0.0.0:8000/analyze/headline", headers=headers,params=headline_payload)

    manual_article = ""
    article_payload = {"article":manual_article,
            "datetime":"12/07/2022",
            "callback_url":""}
    requests.post("http://0.0.0.0:8000/analyze/article", headers=headers,params=article_payload)