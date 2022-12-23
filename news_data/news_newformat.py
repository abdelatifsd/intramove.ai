def new_magic(date_data: str):
    split_data = date_data.split("\n")
    split_data = [data for data in split_data if data != ""]

    headlines = []
    articles = []
    dividers = []
    for index in range(len(split_data)):
        if (index + 1) % 3 == 0:
            split_data[index] = "divider"

    split_data = [data for data in split_data if data != "divider"]

    headlines = []
    articles = []
    for index, headline in enumerate(split_data):
        if index % 2 == 0:
            headlines.append(split_data[index])
        else:
            articles.append(split_data[index])

    return articles, headlines


news_string = """
Wall Street Rally Pauses after GDP RevisionUnited States Stock Market
US stocks traded sharply lower on Thursday, with the Dow Jones losing nearly 350 points, the S&P 500 falling 1.2% and the Nasdaq 1.6%, as fresh economic data raised concerns that further monetary tightening would be necessary which could push the economy into a recession. The final estimate for GDP growth showed the US economy expanded 3.2% in Q3, higher than 2.9% in the second release. At the same time, the claims report continued to point to a healthy labor market, which together with a stronger GDP number, strengthens the case for the Fed to continue to raise interest rates and eventually resort to more aggressive policy. On the corporate front, shares of Micron Technology fell nearly 3% after the company forecasted a bigger-than-expected loss for the current period. On Wednesday, the three major averages booked a strong 1.5% gain, but the rebound proved to be short-lived. So far this month, the Dow is down nearly 3%, the S&P 500 over 4% and the Nasdaq almost 6%.
11 minutes ago
Brazilian Equities on Cautious NoteBrazil Stock Market
Brazil’s benchmark Ibovespa was trading near the flatline around 107,300 after a positive start on Thursday, as investors turned more cautious ahead of the highly expected announcement of new ministers by President-elect Luiz Inacio Lula da Silva while also digesting the approval of the Transition PEC. Brazil's Congress late on Wednesday gave its final approval to a constitutional amendment increasing the government spending cap to maintain welfare payouts to poor families next year. The bill backed by Lula's transition team is set to raise Brazil's spending ceiling by BRL 145 billion for one year to fund monthly payments of 600 reais under the "Bolsa Familia" welfare program and to readjust the minimum wage above inflation. On the corporate front, IRB was the worst performer, with its shares falling almost 9%, followed by Dexco and Americanas, down over 2% each. By contrast, Sabesp and Banco Pan advanced the most, rising around 4% each.
16 minutes ago
"""
articles, headlines = new_magic(news_string)


news_cache = {"12/22/2022": {"headlines": headlines, "articles": articles}}
