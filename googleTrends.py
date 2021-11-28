from pytrends.request import TrendReq
from matplotlib import pyplot
import pandas as pd
import time
import datetime
from datetime import datetime, date, time


pytrend = TrendReq(hl='en-US', tz=360)

all_keywords = ['msft','sony','aapl','amzn']

keywords = []

timeframes = ['today 5-y','today 12-m','today 3-m','today 1-m']

#print('Average interest of the Past 3 months:')

def check_trends():
    pytrend.build_payload(keywords, cat=0, timeframe = timeframes[2],  geo='US')


    data = pytrend.interest_over_time()
    mean = round(data.mean(),2)
    print(kw + ': ' +str(mean[kw]))

for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()