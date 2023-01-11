import requests
import json
from news_data import news_newformat

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

### CHECK THIS FIRST ###
manual = True
### CHECK THIS FIRST ###


if not manual:

    for date, headline_article_dict in news_newformat.news_cache.items():
        
        headlines = headline_article_dict["headlines"]
        articles = headline_article_dict["articles"]

        
        assert len(headlines) == len(articles), "length mismatch"

        for index in range(len(headlines)):
            headline_payload = {"headline":headlines[index] ,
                        "date_time":date,
                        "callback_url":""}
            requests.post("http://0.0.0.0:8000/analyze/headline", headers=headers,params=headline_payload)


    for date, headline_article_dict in news_newformat.news_cache.items():
        
        headlines = headline_article_dict["headlines"]
        articles = headline_article_dict["articles"]

        for index in range(len(headlines)):
            article_payload = {"article":articles[index] ,
                                "date_time":date,
                                "callback_url":""}
            requests.post("http://0.0.0.0:8000/analyze/article", headers=headers,params=article_payload)
else:
    """headline_payload = {"headline":"Ibovespa Rallies for 5th SessionBrazil Stock Market" ,
                        "date_time":"12/07/2022",
                        "callback_url":""}
    response = requests.post("http://0.0.0.0:8000/analyze/headline", headers=headers,params=headline_payload)
    print(response.json())"""
    article = """The S&P/TSX Composite index extended early advances and closed 0.8% higher at 19,500 on Friday, notching a 0.3% increase on the week and outperforming its US counterparts with gains for energy producers and banks. In the meantime, investors digested domestic growth data, pointing to a stall in November and confirming that the Canadian economy expanded by 0.1% in October as growth in services-producing industries offset losses for goods-producing industries. Oil companies soared 4% to lead the gains in the session, tracking the second consecutive weekly increase for crude oil benchmarks. Toronto’s heavyweight banking and mining sectors also booked gains. On the other hand, concerns about tighter monetary policy continued to press the technology sector, leading losses for the day with a 3% slide for Shopify. The Toronto Exchange will be closed on Monday and Tuesday for holidays."""
    article_payload = {"article":article,
            "date_time":"12/07/2022",
            "callback_url":""}
    response = requests.post("http://0.0.0.0:8000/analyze/article", headers=headers,params=article_payload)
    print(response.json())