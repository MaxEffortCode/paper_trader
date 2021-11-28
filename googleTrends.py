from pytrends.request import TrendReq
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import time
import datetime
from datetime import datetime, date, time


pytrend = TrendReq(hl='en-US', tz=360)

all_keywords = ['msft','sony','aapl','amzn']

keywords = []

timeframes = ['today 5-y','today 12-m','today 3-m','today 1-m']
print('Select how far back you would like to research the trends.')
x = int(input('1) 5 years 2) 12 months 3) 3 months 4) 1 month: ')) - 1

while x > 3 or x < 0:
    x = int(input('ok ret**d, pick a number between 1 and 4: ')) - 1

#Checks the trends
def check_trends():
    pytrend.build_payload(keywords, cat=0, timeframe = timeframes[x],  geo='US')


    data = pytrend.interest_over_time()
    #print(data)

    #The closer to 100 the mean value is, the more stable a keyword is
    mean = round(data.mean(numeric_only=True),2)

    print('The average of ' + kw + ': ' +str(mean[kw]))
    #if statment triggered if the time frame is 5 years
    if x == 0:
        avg = round(data[kw][-52:].mean(),2)
        #trend indicates the percentage increase or decrease of interest over the last year
        trend = round(((avg/mean[kw])-1)*100,2)
        print('The last year interest of ' + kw + ' compared to the last 5 years ' + 'has changed by ' + str(trend) + '%.')



#evaluate each keyword individually
for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()

