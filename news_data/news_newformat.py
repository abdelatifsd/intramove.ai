def new_magic(date_data:str):
  split_data = date_data.split("\n")
  split_data = [data for data in split_data if data != ""]

  headlines = []
  articles = []
  dividers = []
  for index in range(len(split_data)):
    if (index+1) % 3 == 0:
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
Ibovespa Rallies for 5th SessionBrazil Stock Market
Brazil’s benchmark Ibovespa closed 2% higher at 109,670 on Friday, extending gains for the fifth straight session with support from banks and energy companies as investors welcomed cooler-than-expected mid-month inflation data. Consumer prices in Brazil rose by 5.9% annually in the first half of December, well below the peak of 12.2% hit in May and raising hopes that the Selic rate could be lowered in 2023 despite the sharp increase in public spending for the upcoming government. The Ibovespa closed the week 6.7% higher, booking the best week in over two months as amendments to the next government’s budget were approved for one year instead previous expectations of two years. The change limited the amount of stimulus that may be passed in the near future, raising hopes of lower inflation and interest rates.
3 days ago
Toronto Shares Close Week in the GreenCanada Stock Market
The S&P/TSX Composite index extended early advances and closed 0.8% higher at 19,500 on Friday, notching a 0.3% increase on the week and outperforming its US counterparts with gains for energy producers and banks. In the meantime, investors digested domestic growth data, pointing to a stall in November and confirming that the Canadian economy expanded by 0.1% in October as growth in services-producing industries offset losses for goods-producing industries. Oil companies soared 4% to lead the gains in the session, tracking the second consecutive weekly increase for crude oil benchmarks. Toronto’s heavyweight banking and mining sectors also booked gains. On the other hand, concerns about tighter monetary policy continued to press the technology sector, leading losses for the day with a 3% slide for Shopify. The Toronto Exchange will be closed on Monday and Tuesday for holidays.
3 days ago
US Stocks Close Higher on FridayUnited States Stock Market
The Dow Jones erased early losses and closed 170 points higher while the S&P 500 added 0.6% on Friday with support from energy shares, as investors continued to digest the latest economic data for hints on the Federal Reserve’s path. The core PCE price index, the Fed’s preferred inflation gauge, slowed more than the FOMC had forecasted in its projections last week. Meanwhile, personal spending edged higher from the prior month and durable goods orders shrank the most in two years. Still, concerns that the Fed will maintain its hawkish guidance for next year persisted after GDP growth and quarterly PCE inflation figures were revised higher yesterday, pressuring the tech-heavy Nasdaq to underperform and close marginally above the flatline. So far in December, the Dow Jones is down 4%, the S&P 500 shed 5.9%, and the Nasdaq tumbled 8.7%, with the three major averages on track for their worst yearly performance since 2008. Markets will be closed on Monday for the Christmas holiday.
3 days ago
El Salvador GDP Grows by 2.1% in Q3El Salvador GDP Annual Growth Rate
The economy of El Salvador expanded by 2.1 percent in the third quarter of 2022, the least since the fourth quarter of 2020 and easing from the downwardly revised 2.4 percent growth in the previous period. Contractions were noted for government expenditure (-1.8 percent vs -7.7 percent in Q2), while slower growth took place in household consumption (1.9 percent vs 2.6 percent). In the meantime, a faster increase in gross fixed capital formation (10.4 percent vs 6.9 percent) limited the slowdown in El Salvador’s GDP. Also, net foreign demand contributed positively to the GDP as exports (12.7 percent) grew faster than imports (2.5 percent). On a quarterly basis, the economy grew by 0.5 percent after contracting 0.5 percent in the prior quarter.
3 days ago
Costa Rica GDP Growth Slows FurtherCosta Rica GDP Annual Growth Rate
Costa Rica’s GDP advanced 3.3 percent year-on-year in the third quarter of 2022, the least since March 2021 and slowing from the 5.7 percent in the previous quarter. Output slowed for professional and scientific activities (7.9 percent vs 11.3 percent in Q2) and wholesale and retail trade (3.2 percent vs 4.1 percent), while it contracted for construction (-14 percent vs -8 percent), agriculture and fishing (-1.2 percent vs -1.1 percent), and mining and quarrying (-0.2 percent vs -3 percent). On the other hand, GDP growth accelerated for manufacturing (5 percent vs 4.1 percent). On a seasonally adjusted quarterly basis, the Costa Rican economy contracted by 0.2 percent.
3 days ago
Colombian Business Confidence Rebounds in NovemberColombia Business Confidence
The industrial confidence indicator in Colombia improved to 0.1 in November of 2022 from the 17-month low of -0.4 in the prior month. Pessimism regarding the current volume of orders fell sharply (-2.9 vs -10.9 in October). On the other hand, expected production in the next three months retreated (2 vs 13.5) and the level of stocks of finished goods at the end of the month declined (-1.2 vs 3.7).
3 days ago
Wall Street Cut Early LossesUnited States Stock Market
The Dow Jones erased early losses and hovered 100 points higher while the S&P 500 was 0.3% up on Friday with support from energy shares, as investors continued to digest the latest economic data for hints on the Federal Reserve’s path. The core PCE price index, the central bank’s preferred inflation gauge, slowed broadly in line with analysts’ expectations in November. Meanwhile, personal spending edged higher from the prior month and durable goods orders shrank the most in two years. Still, concerns that the Fed will maintain its hawkish guidance for next year persisted after GDP growth and PCE inflation figures were revised higher yesterday, pressuring the tech-heavy Nasdaq to underperform and hover below the flatline. So far in December, the Dow Jones is down 4%, the S&P 500 shed 5.9%, and the Nasdaq tumbled 8.7%, with the three major averages on track for their worst yearly performance since 2008.
3 days ago
French Shares Underperform on FridayFrance Stock Market
The benchmark CAC 40 index closed 0.2% lower at 6,500 on Friday, underperforming other European bourses with pressure from consumer discretionary stocks as investors digested a slower PCE price index in the US. Paris’s heavyweight luxury brands closed sharply lower amid further Covid concerns in the sector’s top consumer China, with LVMH and Hermes sliding 1.5% each. Authorities in Beijing stated that the country may have registered around 37 million Covid cases in one day, extending the economy’s period of inactivity and driving demand for luxury goods to decline. Still, the CAC 40 index added nearly 1% on the week. On the data front, producer prices in France accelerated by 1.2% month-over-month in November, after contracting by 0.2% in the previous month. The Paris Stock Exchange will be closed on Monday for holidays.
3 days ago
Spain Stocks Steady on FridaySpain Stock Market
The IBEX 35 closed at 8271 on Friday, little changed from the previous session, in line with its European peers as the market remained cautious ahead of the holiday season amidst concerns of further monetary tightening and its impact on the economy. Domestically, producer prices in Spain rose at a slower 20.7% in November 2022, the least since August 2021. Meanwhile, the country's GDP growth was revised lower to show a meager 0.1% expansion in Q3. On the week, the Spanish index rose nearly 2%, recovering from two consecutive weeks of losses. The IBEX 35 will be closed on December 26th.
3 days ago
Milan Shares Close Week HigherItaly Stock Market
The FTSE MIB closed a choppy, low-volume session 0.2% higher at 23,870 on Friday, notching a 0.8% jump on the week with support from energy, utility, and financial shares ahead of the Italian government’s confidence vote on the expansionary 2023 budget. While remaining within the EU’s recovery framework, the budget’s expansion will widen the next year’s deficit to 4.5% of GDP from the 3.4% budget set in September, allocating more than EUR 21 billion to aid households and businesses with high energy bills. Utilities extended their gains and closed in the green, as the extended downturn for TTF gas prices reduced the likelihood of the EU’s price cap being triggered. Banks also closed sharply higher. Banco BPM added 0.2% following news it finalized the long-term non-life insurance deal with Credit Agricole. Milan's bourse will close on Monday for St. Stephen's Day celebrations.
3 days ago
European Bourses Close Week on a Muted NoteGermany Stock Market
European equity markets closed roughly flat in choppy trading on Friday, after losing nearly 1% in the previous session, as traders continue to worry that interest rates will need to stay elevated for a longer period, which could hurt the economy even further. Gains across basic materials, real estate, industrials and energy were offset by losses in consumer, technology and utilities shares. On the week, the region-wide STOXX 600 added 0.6%, after two straight weeks of losses. Major bourses in Europe will be closed for a holiday on Monday.
3 days ago
Russian Stocks Close Week LowerRussia Stock Market
The ruble-based MOEX Russia index closed flat at 2,124 on Friday, notching a 0.4% retreat on the week as losses for oil shares offset gains for metallurgists as investors continued to assess the grim outlook for the Russian economy. Oil producers Surgut and Transneft slid nearly 2% each to lead the losses in the sector as soaring Covid cases in top consumer China and Western sanctions dent demand for Russian energy. Data by Reuters showed that exports of oil from Russian Baltic ports are expected to decline by 20% month-on-month in December amid the start of the EU’s oil embargo and the G7’s EUR 60 price ceiling. Meanwhile, export-heavy Russian miners and metallurgists closed the session and the week in the green as the ruble’s slide benefited the outlook on foreign sales. In the meantime, Gazprom closed the day with a 2.6% jump after shareholders approved the firm’s board dividend recommendations for oil subsidiary Gazprom Neft.
3 days ago
South African Stocks End on Positive NoteSouth Africa Stock Market
The JSE FTSE All Share index gained some ground to close about 0.4% higher at 73,493 on Friday, as strength in resource-linked stocks and financials more than offset losses in tech stocks. Meanwhile, investors remained cautious amid the prospect of continued aggressive tightening by major central banks until inflation is under control while keeping an eye on the worsening Covid-19 situation in China. The JSE closed the week about 0.7% higher. The JSE will be closed on December 26th and 27th for the Christmas holidays.
3 days ago
Canada Government Budget Gap Narrows in OctoberCanada Government Budget Value
Canada’s government budget deficit narrowed to CAD 1.9 billion in October of 2022 from CAD 3.68 billion in the corresponding month of the previous year. For the first seven months of the 2022/23 fiscal year, Canada recorded a government budget deficit of CAD 174 million. Revenues rose 17.6% on a broad-based improvement in income streams while program expenses dropped 15.6%, largely reflecting lower transfers to individuals and businesses as COVID-19 support wound down. Public debt charges increased 35.7% this fiscal year, primarily driven by higher interest rates and higher inflation adjustments on real return bonds, which have a coupon that is linked to the level of the consumer price index.
3 days ago
Baltic Exchange Dry Index Falls for 2nd Day, Posts Biggest Drop since 2015Commodity
The Baltic Dry Index, which measures the cost of shipping goods worldwide, slumped 8.2% to an over one-week low of 1,515 points on Friday, the second day of losses. The capesize index, which tracks iron ore and coal cargos of 150,000 tonnes, tumbled 13.9% to mark its worst day since late August at 2,261 points; and the panamax index, which tracks about 60,000 to 70,000 tonnes of coal and grains cargoes, fell 1.8% to 1,535 points. At the same time, the supramax index shed 21 points to 1,062 points. The main index plunged 13.9% this quarter and 31.7% for the year, the most since 2015, on worries about the impact of fresh covid-19 outbreaks in China on demand. The Baltic Exchange will not publish data for the main index from December 26th until January 2nd, 2023.
3 days ago
US Building Permits Revised Slightly Higher in NovemberUnited States Building Permits
Building permits in the United States tumbled 10.6 percent from a month earlier to a seasonally adjusted annual rate of 1.351 million in November 2022, the lowest level since June 2020 and compared to a preliminary estimate of 1.342 million, revised data showed. Permits, a proxy for future construction, have been falling as soaring prices and rising mortgage rates hit demand and activity. Approvals of units in the multi-family segment were revised up to 0.570 million from 0.561 million in earlier estimates; while permits for single-family units were unchanged at 0.781 million. Permits fell in the Midwest (-5.2% vs -6.2% in early estimates), the South (-12.4% vs 12.2%) and the West (-14.8% vs -16.4%) but rose in the Northeast (5.4% vs 1.8%).
3 days ago
UK Stocks Little Changed Ahead Long WeekendUnited Kingdom Stock Market
The FTSE 100 closed little changed in a shortened session on Friday, after a 0.4% loss the day before with the energy sector leading gains. Also, auto stocks added 0.4% after the latest data showed UK car production rose 5.7% in November, the second straight month of increases. In corporate headlines, Hurricane Energy Plc rose 2.6% after activist investor Crystal Amber Fund sent a notice to the group to convene a general meeting proposing leadership change. On the week, the London index advanced almost 2%. The London Stock Exchange will be closed on Monday and Tuesday for the holidays.
3 days ago
US New Home Sales Rise to 3-Month HighUnited States New Home Sales
New home sales in the United States unexpectedly surged 5.8% to a seasonally adjusted annual rate of 640K in November of 2022, the highest in three months and beating market forecasts of 600K. Sales for October were revised down to 605K from an initial estimate of 632K. In November, sales jumped in the West (27.6% to 171K) and the Midwest (21.3% to 57K) but fell in the Northeast (-8.5% to 43K) and the South (-2.1% to 369K). The median price of new houses sold was $471,200, while the average sales price was $543,600. There were 461,000 houses left to sell, up 18.2% from one year ago and corresponding to 8.6 months of supply at the current sales rate.
3 days ago
Michigan Consumer Sentiment Higher than ExpectedUnited States Consumer Confidence
The University of Michigan consumer sentiment for the US was revised higher to 59.7 in December of 2022 from a preliminary of 59.1. The gauge for expectations was revised higher to 59.9 from 58.4 while the current conditions subindex was revised lower to 59.4 from 60.2. Meanwhile, inflation expectations for the year were revised lower to 4.4% from 4.6% in the preliminary estimate and the 5-year outlook was revised lower to 2.9% from 3%.
3 days ago
Canadian Shares Hover Flat on FridayCanada Stock Market
The S&P/TSX Composite index hovered at the flatline at the 19,350 mark on Friday, outperforming its US counterparts as gains for energy producers and banks offset losses for technology companies and miners. In the meantime, investors digested domestic growth data, pointing to a stall in November and confirming that the Canadian economy saw a 0.1% expansion in October as growth in services-producing industries offset losses for goods-producing industries. Oil companies led the gains in the session, jumping 1.5% on average as crude oil prices rose sharply to increase for the second consecutive week. Toronto’s heavyweight banking sector also booked gains. On the other hand, concerns about tighter monetary policy continued to press the technology sector, leading the losses of the day. On the week, Canada’s benchmark equity index is set to drop 0.5%. The Toronto Exchange will be closed on Monday and Tuesday for holidays.
3 days ago
"""
articles, headlines =  new_magic(news_string)


news_cache = {"12/23/2022":{"headlines":headlines,"articles":articles}}